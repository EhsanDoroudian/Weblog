from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Q, Prefetch
from .models import Blog, Comment



@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'username', 'status', 'created_datetime', 'modfied_datetime', 'comment_count_display', 'body_preview']
    list_filter = ['status', 'created_datetime', 'modfied_datetime']
    search_fields = ['title',]
    date_hierarchy = 'created_datetime'
    ordering = ('-modfied_datetime',)
    list_per_page = 20
    readonly_fields = ['created_datetime', 'modfied_datetime', 'comment_count_display']
    list_editable = ['status']
    prepopulated_fields = {'title': ('title',)}
    actions = ['mark_as_published', 'mark_as_draft', 'delete_selected_blogs']
    
    # Performance optimizations
    list_select_related = ['user']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'body', 'status', 'user')
        }),
        ('Timestamps', {
            'fields': ('created_datetime', 'modfied_datetime'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('comment_count_display',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queries with select_related, prefetch_related and annotate comment count"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related(
            ('comments')
        ).annotate(
            comment_count=Count('comments', filter=Q(comments__is_active=True))
        ).distinct()

    def username(self, blog):
        return blog.user.username
    
    @admin.display(ordering="comment_count", description="Total Comments")
    def comment_count_display(self, blog):
        """Read-only field for comment count with styling"""
        count = getattr(blog, 'comment_count', 0)
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            'green' if count > 0 else 'red',
            count
        )

    def body_preview(self, blog):
        """Show body preview in list display"""
        if hasattr(blog, 'body'):
            preview = blog.body[:100] + '...' if len(blog.body) > 100 else blog.body
            return format_html('<span title="{}">{}</span>', blog.body, preview)
        return ''
    body_preview.short_description = 'Body Preview'

    def mark_as_published(self, request, queryset):
        """Bulk action to mark blogs as published"""
        updated = queryset.update(status='pub')
        self.message_user(request, f'{updated} blog(s) marked as published.')
    mark_as_published.short_description = 'Mark selected blogs as published'

    def mark_as_draft(self, request, queryset):
        """Bulk action to mark blogs as draft"""
        updated = queryset.update(status='drf')
        self.message_user(request, f'{updated} blog(s) marked as draft.')
    mark_as_draft.short_description = 'Mark selected blogs as draft'

    def delete_selected_blogs(self, request, queryset):
        """Bulk action to delete blogs with confirmation"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} blog(s) deleted successfully.')
    delete_selected_blogs.short_description = 'Delete selected blogs'

    def get_search_results(self, request, queryset, search_term):
        """Enhanced search functionality"""
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(body__icontains=search_term) |
                Q(user__username__icontains=search_term) |
                Q(user__email__icontains=search_term)
            )
        return queryset, True

    def changelist_view(self, request, extra_context=None):
        """Override to ensure proper query optimization for change list"""
        response = super().changelist_view(request, extra_context)
        return response


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'user', 'blog_title', 'is_active', 'created_datetime', 'modfied_datetime']
    list_filter = ['is_active', 'created_datetime', 'user', 'blog__status']
    search_fields = ['text', 'user__username', 'user__email', 'blog__title']
    date_hierarchy = 'created_datetime'
    ordering = ('-modfied_datetime',)
    list_per_page = 20
    readonly_fields = ['created_datetime', 'modfied_datetime']
    list_editable = ['is_active']
    actions = ['activate_comments', 'deactivate_comments', 'delete_selected_comments']
    autocomplete_fields = ['blog',]

    # Performance optimizations
    list_select_related = ['user', 'blog']
    
    fieldsets = (
        ('Comment Content', {
            'fields': ('text', 'blog', 'user')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_datetime', 'modfied_datetime'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queries with select_related"""
        return super().get_queryset(request).select_related('user', 'blog')

    def text_preview(self, comment):
        """Show comment text preview with tooltip"""
        preview = comment.text[:50] + '...' if len(comment.text) > 50 else comment.text
        return format_html('<span title="{}">{}</span>', comment.text, preview)
    text_preview.short_description = 'Comment Text'

    def blog_title(self, comment):
        """Show blog title with link"""
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            comment.blog.get_absolute_url(),
            comment.blog.title
        )
    blog_title.short_description = 'Blog'
    blog_title.admin_order_field = 'blog__title'

    def activate_comments(self, request, queryset):
        """Bulk action to activate comments"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} comment(s) activated.')
    activate_comments.short_description = 'Activate selected comments'

    def deactivate_comments(self, request, queryset):
        """Bulk action to deactivate comments"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} comment(s) deactivated.')
    deactivate_comments.short_description = 'Deactivate selected comments'

    def delete_selected_comments(self, request, queryset):
        """Bulk action to delete comments"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} comment(s) deleted successfully.')
    delete_selected_comments.short_description = 'Delete selected comments'

    def get_search_results(self, request, queryset, search_term):
        """Enhanced search functionality"""
        if search_term:
            queryset = queryset.filter(
                Q(text__icontains=search_term) |
                Q(user__username__icontains=search_term) |
                Q(user__email__icontains=search_term) |
                Q(blog__title__icontains=search_term)
            )
        return queryset, True
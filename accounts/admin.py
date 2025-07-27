from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count, Q
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import CustomUserModel
from accounts.forms import CustomUserCreateForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    model = CustomUserModel
    form = CustomUserChangeForm
    add_form = CustomUserCreateForm
    
    # Enhanced list display
    list_display = [
        'username', 'email', 'full_name', 'age', 'gender', 
        'blog_count', 'comment_count', 'is_staff', 'is_active', 'date_joined'
    ]
    
    # Enhanced list filters
    list_filter = [
        'is_staff', 'is_active', 'is_superuser', 'gender', 
        'date_joined', 'last_login', ('groups', admin.RelatedOnlyFieldListFilter)
    ]
    
    # Enhanced search fields
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    # Performance optimizations
    list_per_page = 25
    ordering = ('-date_joined',)
    
    # Enhanced fieldsets
    fieldsets = (
        ('Personal Information', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email')
        }),
        ('Additional Information', {
            'fields': ('age', 'gender'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    # Enhanced add fieldsets
    add_fieldsets = (
        ('Account Information', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'age', 'gender'),
        }),
    )
    
    # Enhanced actions
    actions = ['activate_users', 'deactivate_users', 'make_staff', 'remove_staff']

    def get_queryset(self, request):
        """Optimize queries with annotations for blog and comment counts"""
        return super().get_queryset(request).prefetch_related(
            'groups', 'user_permissions'
        ).annotate(
            blog_count=Count('blogs'),
            comment_count=Count('comments', filter=Q(comments__is_active=True))
        ).distinct()

    def full_name(self, obj):
        """Display full name with styling"""
        if hasattr(obj, 'first_name') and hasattr(obj, 'last_name'):
            if obj.first_name and obj.last_name:
                return f"{obj.first_name} {obj.last_name}"
            elif obj.first_name:
                return obj.first_name
            elif obj.last_name:
                return obj.last_name
        return format_html('<span style="color: #999;">Not provided</span>')
    full_name.short_description = 'Full Name'
    full_name.admin_order_field = 'first_name'

    def blog_count(self, obj):
        """Display blog count from annotation"""
        count = getattr(obj, 'blog_count', 0)
        if count > 0:
            return format_html(
                '<a href="{}?user__id__exact={}" style="color: green; font-weight: bold;">{}</a>',
                reverse('admin:blogs_blog_changelist'),
                obj.id,
                count
            )
        return format_html('<span style="color: #999;">{}</span>', count)
    blog_count.short_description = 'Blogs'
    blog_count.admin_order_field = 'blog_count'

    def comment_count(self, obj):
        """Display comment count from annotation"""
        count = getattr(obj, 'comment_count', 0)
        if count > 0:
            return format_html(
                '<a href="{}?user__id__exact={}" style="color: blue; font-weight: bold;">{}</a>',
                reverse('admin:blogs_comment_changelist'),
                obj.id,
                count
            )
        return format_html('<span style="color: #999;">{}</span>', count)
    comment_count.short_description = 'Comments'
    comment_count.admin_order_field = 'comment_count'

    def activate_users(self, request, queryset):
        """Bulk action to activate users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated successfully.')
    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        """Bulk action to deactivate users"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated successfully.')
    deactivate_users.short_description = 'Deactivate selected users'

    def make_staff(self, request, queryset):
        """Bulk action to make users staff"""
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} user(s) granted staff privileges.')
    make_staff.short_description = 'Grant staff privileges to selected users'

    def remove_staff(self, request, queryset):
        """Bulk action to remove staff privileges"""
        updated = queryset.update(is_staff=False)
        self.message_user(request, f'{updated} user(s) staff privileges removed.')
    remove_staff.short_description = 'Remove staff privileges from selected users'

    def get_search_results(self, request, queryset, search_term):
        """Enhanced search functionality"""
        if search_term:
            queryset = queryset.filter(
                Q(username__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term)
            )
        return queryset, True


admin.site.register(CustomUserModel, CustomUserAdmin)

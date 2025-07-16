from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime

from blogs.models import Blog, Comment
from blogs.forms import CommentForm
from accounts.models import CustomUserModel


class TestBlog(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = CustomUserModel.objects.create_user(
            username='user1',
            email='user1@gmail.com',
            age='20',
            password='password1'
        )

        cls.user2 = CustomUserModel.objects.create_user(
            username='user2',
            email='user2@gmail.com',
            age='30',
            password='password2'
        )

        cls.admin = CustomUserModel.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin1234'
        )

        cls.blog1 = Blog.objects.create(
            title = 'Title1',
            user = cls.user1,
            body = 'Body1',
            status = 'pub',
            modfied_datetime=timezone.now() - datetime.timedelta(days=1)
        )        

        cls.blog2 = Blog.objects.create(
            title = 'Title2',
            user = cls.user2,
            body = 'Body2',
            status = 'drf',
            modfied_datetime=timezone.now()
        )

        cls.blog3 = Blog.objects.create(
            title = 'Title3',
            user = cls.user2,
            body = 'Body3',
            status = 'pub',
            modfied_datetime=timezone.now()
        ) 
 

        cls.comment1 = Comment.objects.create(
            blog=cls.blog1,
            user=cls.user2,
            text="Text1",
            is_active=True,
            created_datetime=timezone.now()
        )

        cls.comment2 = Comment.objects.create(
            blog=cls.blog2,
            user=cls.user1,
            text="Text2",
            is_active=False,
            created_datetime=timezone.now()
        )         

    def test_user_information(self):
        self.assertEqual(self.user1.username, 'user1')
        self.assertEqual(self.user1.email, 'user1@gmail.com')
        self.assertEqual(self.user1.age, '20')

        self.assertEqual(self.user2.username, 'user2')
        self.assertEqual(self.user2.email, 'user2@gmail.com')
        self.assertEqual(self.user2.age, '30')

        self.assertEqual(self.comment1.blog, self.blog1)
        self.assertEqual(self.comment1.user, self.user2)
        self.assertEqual(self.comment1.text, "Text1")
        self.assertEqual(self.comment1.is_active, True)
        
        self.assertEqual(self.comment2.blog, self.blog2)
        self.assertEqual(self.comment2.user, self.user1)
        self.assertEqual(self.comment2.text, "Text2")
        self.assertEqual(self.comment2.is_active, False)
        

class TestBlogList(TestBlog):

    def test_blog_list_view(self):
        response = self.client.get('')
        response2 = self.client.get('/blogs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)

    def test_blog_list_name_view(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)

    def test_blog_list_template(self):
        response = self.client.get(reverse('blog_list'))
        self.assertTemplateUsed(response, 'blogs/blogs_list_page.html')
    
    def test_blog_list_view_content(self):
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog1)
        self.assertNotContains(response, self.blog2)
        self.assertIn(self.blog1, response.context["blogs"])
        self.assertNotIn(self.blog2, response.context["blogs"])
    
    def test_blog_list_empty(self):
        Blog.objects.all().delete()
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["blogs"]), 0)
    
    def test_blog_list_pagination(self):
        for i in range(3, 21):
            Blog.objects.create(
                user=self.user1,
                title=f"Title{i}",
                body=f"Body{i}",
                status='pub',
                modfied_datetime=timezone.now()
            )
        response = self.client.get(reverse("blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["blogs"]), 7)
        # Test second page
        response = self.client.get(reverse("blog_list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["blogs"]), 7)
        # Test third page
        response = self.client.get(reverse("blog_list") + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["blogs"]), 6)
    
    def test_blog_list_ordering(self):
        response = self.client.get(reverse("blog_list"))
        blogs = response.context['blogs']
        # Verify books are ordered by modified_datetime descending
        self.assertEqual(blogs[0], self.blog1)  # Newer book first
        self.assertEqual(blogs[1], self.blog3)  # Older book second

class TestBlogDetail(TestBlog):

    def test_blog_detail_url_redirects_unauthenticated_users(self):
        response = self.client.get(f'/blogs/{self.blog2.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/blogs/{self.blog2.id}/')
    
    def test_blog_detail_url_name_redirects_unauthenticated_users(self):
        url = reverse('blog_detail', args=[self.blog1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={url}')
    
    def test_blog_detail_view_authenticated(self):
        self.client.force_login(self.user1)  
        response = self.client.get(reverse('blog_detail', args=[self.blog1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blog_detail_page.html')
    
    def test_blog_detail_view_content(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('blog_detail', args=[self.blog1.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.blog1.body)
        self.assertContains(response, self.blog1.user)
        self.assertEqual(response.context['blog'], self.blog1)
        self.assertIsInstance(response.context['comment_form'], CommentForm)


class TestBlogCreate(TestBlog):

    def test_blog_create_view_url_unauthenticated_users(self):
        response = self.client.get('/create/')
        response2 = self.client.get('/blogs/create/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response2.status_code, 302)

        self.assertRedirects(response, '/accounts/login/?next=/create/')
        self.assertRedirects(response2, '/accounts/login/?next=/blogs/create/')

    def test_blog_create_view_name_unauthenticated_users(self):
        response = self.client.get(reverse('blog_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/create/')

    def test_blog_view_authenticated_users(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('blog_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/blog_create_page.html')

    def test_blog_view_form(self):
        self.client.force_login(self.user1)
        url = reverse('blog_create')  
        response = self.client.post(  
            path=url,
            data={
                'title': 'title3', 
                'body': 'body3',
                'status': 'drf',  
            },
            follow=False  # Disable following redirects to check status 302
        )
        
        # Debug: Print form errors if status is not 302
        if response.status_code != 302:
            print("Form errors:", response.context['form'].errors)
        
        self.assertEqual(response.status_code, 302)  # Should redirect
        blog = Blog.objects.last()
        self.assertIsNotNone(blog)  # Ensure blog was created
        self.assertEqual(Blog.objects.last().user, self.user1)
        self.assertEqual(Blog.objects.last().title, 'title3')
        self.assertEqual(Blog.objects.last().body, 'body3')
        self.assertEqual(Blog.objects.last().status, 'drf')

        self.assertEqual(response.url, blog.get_absolute_url())  # Check redirect URL


class TestBlogUpdate(TestBlog):
    pass
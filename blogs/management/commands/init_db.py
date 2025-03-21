from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from tqdm import tqdm
from accounts.models import CustomUserModel
from blogs.models import Blog
from datetime import datetime

class Command(BaseCommand):
    help = "Generates fake blog posts for testing purposes."

    def handle(self, *args, **options):
        # Initialize Faker
        fake = Faker()

        # Delete all existing blogs
        self.delete_existing_blogs()

        # Create a superuser if it doesn't exist
        self.create_superuser()

        # Fetch all users (assuming you have some users in your database)
        users = CustomUserModel.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR("No users found. Please create some users first."))
            return

        # Number of fake blogs to create
        NUM_BLOGS = 50

        # Create fake blog posts with a progress bar
        for _ in tqdm(range(NUM_BLOGS), desc="Creating fake blogs", unit="blog"):
            # Generate fake data
            title = fake.sentence(nb_words=6)  # Generate a title with 6 words
            user = fake.random_element(users)  # Randomly assign a user
            body = fake.paragraph(nb_sentences=10)  # Generate a body with 10 sentences
            status = fake.random_element(elements=("pub", "drf"))  # Randomly choose status

            # Generate a random datetime between 2000 and now
            created_datetime = fake.date_time_between(
                start_date='-23y',  # 23 years ago (2000)
                end_date='now',     # Current time
                tzinfo=timezone.get_current_timezone()  # Use Django's current timezone
            )

            # Create and save the Blog instance
            Blog.objects.create(
                title=title,
                user=user,
                body=body,
                status=status,
                created_datetime=created_datetime,  # Set the random datetime
            )

        self.stdout.write(self.style.SUCCESS(f"{NUM_BLOGS} fake blog posts created successfully!"))

    def delete_existing_blogs(self):
        """Delete all existing blogs."""
        deleted_count, _ = Blog.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} existing blog(s)."))
        
    def create_superuser(self):
        """Create a superuser if it doesn't already exist."""
        username = "admin"
        email = "admin@example.com"
        password = "admin1234"

        if not CustomUserModel.objects.filter(username=username).exists():
            CustomUserModel.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists."))
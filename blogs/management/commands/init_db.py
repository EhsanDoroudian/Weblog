from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from tqdm import tqdm
from accounts.models import CustomUserModel
from blogs.models import Blog

class Command(BaseCommand):
    help = "Generates fake blog posts for testing purposes."

    def handle(self, *args, **options):
        # Initialize Faker
        fake = Faker()

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

            # Create and save the Blog instance
            Blog.objects.create(
                title=title,
                user=user,
                body=body,
                status=status,
            )

        self.stdout.write(self.style.SUCCESS(f"{NUM_BLOGS} fake blog posts created successfully!"))
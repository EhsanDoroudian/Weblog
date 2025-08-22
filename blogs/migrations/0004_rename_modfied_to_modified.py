from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_alter_blog_user_alter_comment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='modfied_datetime',
            new_name='modified_datetime',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='modfied_datetime',
            new_name='modified_datetime',
        ),
    ]

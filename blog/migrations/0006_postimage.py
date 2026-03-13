from django.db import migrations, models
import django.db.models.deletion
from blog.storage_backends import SupabaseStorage


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_visitor'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(storage=SupabaseStorage(), upload_to='post-images/')),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.post')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
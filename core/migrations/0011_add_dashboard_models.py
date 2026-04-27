# Generated migration for dashboard models

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_add_ref_code_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Django Shop', max_length=100)),
                ('site_email', models.EmailField(default='contact@djangoshop.com', max_length=254)),
                ('whatsapp_number', models.CharField(blank=True, max_length=20)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('address', models.TextField(blank=True)),
                ('facebook_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
                ('youtube_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='site/')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='site/')),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('meta_keywords', models.CharField(blank=True, max_length=255)),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('items_per_page', models.IntegerField(default=12)),
                ('enable_reviews', models.BooleanField(default=True)),
                ('enable_wishlist', models.BooleanField(default=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Site Settings',
            },
        ),
        migrations.CreateModel(
            name='SiteImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_type', models.CharField(choices=[('banner', 'Bannière'), ('hero', 'Hero Section'), ('logo', 'Logo'), ('favicon', 'Favicon'), ('marketing', 'Marketing'), ('other', 'Autre')], max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='site-images/')),
                ('description', models.TextField(blank=True)),
                ('alt_text', models.CharField(blank=True, max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['image_type', 'order'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('replied_at', models.DateTimeField(blank=True, null=True)),
                ('reply_message', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 étoile'), (2, '2 étoiles'), (3, '3 étoiles'), (4, '4 étoiles'), (5, '5 étoiles')])),
                ('title', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('is_approved', models.BooleanField(default=False)),
                ('admin_response', models.TextField(blank=True)),
                ('helpful_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='core.item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'unique_together': {('item', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('discount_type', models.CharField(choices=[('percentage', 'Pourcentage'), ('fixed', 'Montant fixe')], max_length=20)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_uses', models.IntegerField(blank=True, null=True)),
                ('used_count', models.IntegerField(default=0)),
                ('min_order_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('items', models.ManyToManyField(blank=True, to='core.Item')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]

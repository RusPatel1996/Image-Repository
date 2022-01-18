# Generated by Django 4.0.1 on 2022-01-18 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('user_name', models.CharField(max_length=100, unique=True)),
                ('password', models.BinaryField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('height', models.PositiveIntegerField()),
                ('width', models.PositiveIntegerField()),
                ('image', models.ImageField(db_index=True, height_field='height', upload_to='images/', width_field='width')),
                ('thumbnail', models.ImageField(db_index=True, upload_to='thumbnails/')),
                ('image_hash', models.CharField(max_length=50)),
                ('color', models.CharField(choices=[('Any', 'Any'), ('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green'), ('Yellow', 'Yellow'), ('Purple', 'Purple'), ('Cyan', 'Cyan')], default='Any', max_length=7)),
                ('permission', models.CharField(choices=[('All', 'All'), ('Private', 'Private'), ('Public', 'Public')], default='All', max_length=7)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_repository.user')),
            ],
        ),
    ]

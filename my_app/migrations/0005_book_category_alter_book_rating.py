# Generated by Django 4.2.15 on 2024-09-02 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_alter_book_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Mystery', 'Mystery'), ('Thriller', 'Thriller'), ('Science Fiction', 'Science Fiction'), ('Romance', 'Romance'), ('Fantasy', 'Fantasy')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]),
        ),
    ]

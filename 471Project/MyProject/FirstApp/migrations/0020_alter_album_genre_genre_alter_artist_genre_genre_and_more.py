# Generated by Django 4.2.7 on 2023-11-22 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FirstApp', '0019_song_genre_producer_genre_artist_genre_album_genre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album_genre',
            name='genre',
            field=models.CharField(choices=[('POP', 'Pop'), ('ROCK', 'Rock'), ('HIPHOP', 'Hip Hop'), ('RNB', 'R&B'), ('JAZZ', 'Jazz'), ('CLASSICAL', 'Classical'), ('FOLK', 'Folk'), ('PUNK', 'Punk'), ('METAL', 'Metal'), ('ELECTRONIC', 'Electronic'), ('COUNTRY', 'Country'), ('SOUL', 'Soul')], max_length=50),
        ),
        migrations.AlterField(
            model_name='artist_genre',
            name='genre',
            field=models.CharField(choices=[('POP', 'Pop'), ('ROCK', 'Rock'), ('HIPHOP', 'Hip Hop'), ('RNB', 'R&B'), ('JAZZ', 'Jazz'), ('CLASSICAL', 'Classical'), ('FOLK', 'Folk'), ('PUNK', 'Punk'), ('METAL', 'Metal'), ('ELECTRONIC', 'Electronic'), ('COUNTRY', 'Country'), ('SOUL', 'Soul')], max_length=50),
        ),
        migrations.AlterField(
            model_name='producer_genre',
            name='genre',
            field=models.CharField(choices=[('POP', 'Pop'), ('ROCK', 'Rock'), ('HIPHOP', 'Hip Hop'), ('RNB', 'R&B'), ('JAZZ', 'Jazz'), ('CLASSICAL', 'Classical'), ('FOLK', 'Folk'), ('PUNK', 'Punk'), ('METAL', 'Metal'), ('ELECTRONIC', 'Electronic'), ('COUNTRY', 'Country'), ('SOUL', 'Soul')], max_length=50),
        ),
        migrations.AlterField(
            model_name='song_genre',
            name='genre',
            field=models.CharField(choices=[('POP', 'Pop'), ('ROCK', 'Rock'), ('HIPHOP', 'Hip Hop'), ('RNB', 'R&B'), ('JAZZ', 'Jazz'), ('CLASSICAL', 'Classical'), ('FOLK', 'Folk'), ('PUNK', 'Punk'), ('METAL', 'Metal'), ('ELECTRONIC', 'Electronic'), ('COUNTRY', 'Country'), ('SOUL', 'Soul')], max_length=50),
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-10 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jmeno', models.CharField(max_length=100)),
                ('prijmeni', models.CharField(max_length=100)),
                ('narozeni', models.DateField()),
                ('umrti', models.DateField(blank=True, null=True)),
                ('zivotopis', models.TextField()),
                ('fotografie', models.ImageField(upload_to='autori/')),
            ],
        ),
        migrations.CreateModel(
            name='Kniha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titul', models.CharField(max_length=100)),
                ('obsah', models.TextField()),
                ('pocet_stran', models.IntegerField()),
                ('rok_vydani', models.IntegerField()),
                ('autor', models.ManyToManyField(to='library.autor')),
            ],
        ),
        migrations.CreateModel(
            name='Vydavatelstvi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazev', models.CharField(max_length=100)),
                ('adresa', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Zanr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazev', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.AddField(
            model_name='kniha',
            name='vydavatelstvi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.vydavatelstvi'),
        ),
        migrations.AddField(
            model_name='kniha',
            name='zanr',
            field=models.ManyToManyField(to='library.zanr'),
        ),
    ]

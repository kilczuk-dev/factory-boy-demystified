# Generated by Django 3.0.4 on 2020-03-26 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('dob', models.DateTimeField()),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N/B', 'Non-Binary')], max_length=100)),
                ('government_id', models.CharField(max_length=20, unique=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='championship.Club')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('players', models.ManyToManyField(related_name='tournaments', to='championship.Player')),
            ],
        ),
    ]

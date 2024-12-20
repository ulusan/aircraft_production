# Generated by Django 5.1.4 on 2024-12-20 14:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('wing', 'Wing'), ('fuselage', 'Fuselage'), ('tail', 'Tail'), ('avionics', 'Avionics')], max_length=50)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('is_used', models.BooleanField(default=False)),
                ('aircraft', models.CharField(choices=[('tb2', 'TB2'), ('tb3', 'TB3'), ('akinci', 'AKINCI'), ('kizilelma', 'KIZILELMA')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('tb2', 'TB2'), ('tb3', 'TB3'), ('akinci', 'AKINCI'), ('kizilelma', 'KIZILELMA')], max_length=50, unique=True)),
                ('produced_date', models.DateTimeField(auto_now_add=True)),
                ('parts', models.ManyToManyField(related_name='aircrafts', to='parts.part')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('wing', 'Wing Team'), ('fuselage', 'Fuselage Team'), ('tail', 'Tail Team'), ('avionics', 'Avionics Team'), ('assembly', 'Assembly Team')], max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('users', models.ManyToManyField(related_name='teams', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='part',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='parts.team'),
        ),
    ]

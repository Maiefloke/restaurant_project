# Generated by Django 5.2.1 on 2025-06-02 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='image',
        ),
        migrations.AddField(
            model_name='dish',
            name='category',
            field=models.CharField(choices=[('Сети', 'Сети'), ('Роли', 'Роли'), ('Супи', 'Супи'), ('Напої', 'Напої')], default='Сети', max_length=50),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description',
            field=models.TextField(),
        ),
    ]

# Generated by Django 3.0.3 on 2020-07-29 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='quiz.Quiz'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-05-25 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0007_remove_result_questions_result_questions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="result",
            name="questions",
            field=models.ManyToManyField(related_name="quest", to="quiz.question"),
        ),
    ]

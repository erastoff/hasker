# Generated by Django 5.0.1 on 2024-02-04 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("question", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="question.question",
            ),
        ),
    ]
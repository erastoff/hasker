# Generated by Django 5.0.1 on 2024-02-18 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("question", "0004_questionvote"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionvote",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="qvotes",
                to="question.question",
            ),
        ),
    ]

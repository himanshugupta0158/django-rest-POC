# Generated by Django 4.2.7 on 2023-11-21 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_student_passby_student_marks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='marks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
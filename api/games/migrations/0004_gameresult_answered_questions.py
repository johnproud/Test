# Generated by Django 3.2.7 on 2021-10-08 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_gameresult_responses'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresult',
            name='answered_questions',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

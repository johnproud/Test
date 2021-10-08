# Generated by Django 3.2.7 on 2021-10-08 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nomenclatures', '0002_auto_20211008_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='is_valid_response',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='response',
            name='points_earned',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='response',
            name='choice_response',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='nomenclatures.answerchoice'),
        ),
        migrations.AlterField(
            model_name='response',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nomenclatures.question'),
        ),
    ]

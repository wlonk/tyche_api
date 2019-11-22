# Generated by Django 2.1.3 on 2019-11-22 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_server_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='prefix',
            field=models.CharField(choices=[('?', '?'), ('!', '!'), (':', ':'), (';', ';'), ('~', '~'), ('%', '%')], default='?', max_length=1),
        ),
    ]
# Generated by Django 4.2.1 on 2023-07-29 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'permissions': (('add_table', 'can add game table'), ('remove_table', 'can remove game table'), ('add_player_table', 'add player to exists table'), ('retrieve_table', 'show table status'), ('remove_player_table', 'remove player from the table'), ('manage_player', ' manage player'))},
        ),
    ]
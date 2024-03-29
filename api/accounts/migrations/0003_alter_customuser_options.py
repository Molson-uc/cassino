# Generated by Django 4.2.1 on 2023-07-29 16:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_customuser_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={
                "permissions": (
                    ("add_table", "can add game table"),
                    ("remove_table", "can remove game table"),
                    ("add_player_table", "add player to exists table"),
                    ("remove_player_table", "remove player from the table"),
                    ("manage_player", " manage player"),
                )
            },
        ),
    ]

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("links", "0002_link_updated_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="link",
            old_name="sortorder",
            new_name="boost",
        ),
    ]

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("contents", "0035_alter_servicepage_options_remove_aboutpage_cta_label_and_more"),
    ]

    operations = [
        # Сначала удаляем зависимые модели, потом базовую
        migrations.DeleteModel(name="ServicesBlockPlacement"),
        migrations.DeleteModel(name="ServiceItem"),
        migrations.DeleteModel(name="ServicesBlock"),
    ]

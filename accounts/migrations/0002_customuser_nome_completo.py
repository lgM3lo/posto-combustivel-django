from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="nome_completo",
            field=models.CharField(default="", max_length=255, verbose_name="Nome completo"),
        ),
    ]

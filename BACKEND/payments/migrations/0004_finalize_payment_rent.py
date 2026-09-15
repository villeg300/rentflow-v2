from django.db import migrations, models


def verify_payments_have_rent(apps, schema_editor):
    Payment = apps.get_model("payments", "Payment")

    missing_rent = Payment.objects.filter(rent__isnull=True).count()

    if missing_rent > 0:
        raise RuntimeError(
            f"{missing_rent} paiement(s) n'ont pas de Rent associé."
        )


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0003_link_payments_to_rent"),
    ]

    operations = [
        migrations.RunPython(
            verify_payments_have_rent,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="payment",
            name="rent",
            field=models.ForeignKey(
                on_delete=models.PROTECT,
                related_name="payments",
                to="leases.rent",
            ),
        ),
        migrations.RemoveField(
            model_name="payment",
            name="lease",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="rent_month",
        ),
    ]
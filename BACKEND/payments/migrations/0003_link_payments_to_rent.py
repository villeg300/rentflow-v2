from django.db import migrations


def link_payments_to_rent(apps, schema_editor):
    Payment = apps.get_model("payments", "Payment")
    Rent = apps.get_model("leases", "Rent")

    payments = Payment.objects.filter(rent__isnull=True)

    for payment in payments:
        rent = Rent.objects.filter(
            lease_id=payment.lease_id,
            period=payment.rent_month,
        ).first()

        if rent:
            payment.rent_id = rent.id
            payment.save(update_fields=["rent"])


def reverse_link_payments_to_rent(apps, schema_editor):
    Payment = apps.get_model("payments", "Payment")

    payments = Payment.objects.exclude(rent__isnull=True)

    for payment in payments:
        payment.lease_id = payment.rent.lease_id
        payment.rent_month = payment.rent.period
        payment.save(update_fields=["lease", "rent_month"])


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0002_payment_rent"),
        ("leases", "0004_rent"),
    ]

    operations = [
        migrations.RunPython(
            link_payments_to_rent,
            reverse_link_payments_to_rent,
        ),
    ]
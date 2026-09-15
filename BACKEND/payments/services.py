from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from leases.models import Rent
from payments.models import Payment


@transaction.atomic
def create_payment(
    *,
    rent: Rent,
    amount: Decimal,
    payment_date,
    payment_method: str,
    reference: str = "",
    note: str = "",
):
    rent = (
        Rent.objects
        .select_for_update()
        .select_related("lease")
        .get(pk=rent.pk)
    )

    if amount <= 0:
        raise ValidationError(
            "Le montant du paiement doit être supérieur à zéro."
        )

    total_paid = sum(
        payment.amount
        for payment in rent.payments.all()
    )

    remaining_amount = rent.amount_due - total_paid
    installments_used = rent.payments.count()

    if remaining_amount <= 0:
        raise ValidationError(
            "Ce loyer est déjà entièrement payé."
        )

    if installments_used >= rent.lease.max_installments:
        raise ValidationError(
            "Le nombre maximal de tranches pour ce loyer est atteint."
        )

    if amount > remaining_amount:
        raise ValidationError(
            "Le montant du paiement dépasse le reste à payer."
        )

    installments_remaining = (
        rent.lease.max_installments - installments_used
    )

    if installments_remaining == 1 and amount != remaining_amount:
        raise ValidationError(
            "La dernière tranche doit correspondre exactement au reste à payer."
        )

    payment = Payment(
        rent=rent,
        amount=amount,
        payment_date=payment_date,
        payment_method=payment_method,
        reference=reference,
        note=note,
    )

    payment.full_clean()
    payment.save()

    return payment
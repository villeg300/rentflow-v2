from django.core.exceptions import ValidationError
from django.db import models

from leases.models import Rent


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Espèces"
        MOBILE_MONEY = "MOBILE_MONEY", "Mobile Money"
        BANK_TRANSFER = "BANK_TRANSFER", "Virement bancaire"
        OTHER = "OTHER", "Autre"

    rent = models.ForeignKey(
        Rent,
        on_delete=models.PROTECT,
        related_name="payments",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    payment_date = models.DateField()
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )
    reference = models.CharField(
        max_length=100,
        blank=True,
    )
    note = models.TextField(
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.amount <= 0:
            raise ValidationError(
                "Le montant du paiement doit être supérieur à zéro."
            )

    def __str__(self):
        return f"{self.amount} FCFA - {self.rent}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="payment_amount_positive",
            ),
        ]
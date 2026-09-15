from django.core.exceptions import ValidationError
from django.db import models

from properties.models import Unit
from tenants.models import Tenant


class Lease(models.Model):
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name="leases",
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="leases",
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    rent_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    deposit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    max_installments = models.PositiveIntegerField(default=1)
    due_day = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError(
                "La date de fin doit être postérieure ou égale à la date de début."
            )

        if self.max_installments < 1:
            raise ValidationError(
                "Le nombre maximal de tranches doit être supérieur ou égal à 1."
            )

        if not 1 <= self.due_day <= 28:
            raise ValidationError(
                "Le jour d'échéance doit être compris entre 1 et 28."
            )

    def __str__(self):
        return f"{self.tenant} - {self.unit}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(end_date__isnull=True)
                    | models.Q(end_date__gte=models.F("start_date"))
                ),
                name="lease_end_date_after_start_date",
            ),
            models.CheckConstraint(
                condition=models.Q(max_installments__gte=1),
                name="lease_max_installments_positive",
            ),
            models.CheckConstraint(
                condition=models.Q(due_day__gte=1)
                & models.Q(due_day__lte=28),
                name="lease_due_day_valid",
            ),
        ]



class Rent(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        PARTIAL = "PARTIAL", "Partiel"
        PAID = "PAID", "Payé"
        LATE = "LATE", "En retard"
    
    lease = models.ForeignKey(
        Lease,
        on_delete=models.PROTECT,
        related_name="rents",
    )
    period = models.DateField()
    amount_due = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_paid(self):
        return sum(
            payment.amount
            for payment in self.payments.all()
        )

    @property
    def remaining_amount(self):
        remaining = self.amount_due - self.total_paid
        return max(remaining, 0)

    @property
    def installments_used(self):
        return self.payments.count()

    @property
    def remaining_installments(self):
        return max(
            self.lease.max_installments - self.installments_used,
            0,
        )
    
    @property
    def status(self):
        from django.utils import timezone

        if self.total_paid >= self.amount_due:
            return self.Status.PAID

        if timezone.localdate() > self.due_date:
            return self.Status.LATE

        if self.total_paid > 0:
            return self.Status.PARTIAL

        return self.Status.PENDING

    def __str__(self):
        return f"{self.lease} - {self.period}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lease", "period"],
                name="unique_rent_per_lease_period",
            ),
            models.CheckConstraint(
                condition=models.Q(amount_due__gt=0),
                name="rent_amount_due_positive",
            ),
        ]
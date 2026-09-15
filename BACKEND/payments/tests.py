from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from leases.models import Lease, Rent
from payments.services import create_payment
from properties.models import Property, Unit
from tenants.models import Tenant
from unittest.mock import patch


class CreatePaymentTests(TestCase):
    def setUp(self):
        self.property = Property.objects.create(
            name="Résidence Test",
            address="Zone du Bois",
            city="Ouagadougou",
        )

        self.unit = Unit.objects.create(
            property=self.property,
            name="A01",
            monthly_rent=Decimal("75000"),
        )

        self.tenant = Tenant.objects.create(
            first_name="Jean",
            last_name="Test",
            phone="70000000",
        )

        self.lease = Lease.objects.create(
            unit=self.unit,
            tenant=self.tenant,
            start_date=date(2026, 10, 1),
            rent_amount=Decimal("75000"),
            deposit_amount=Decimal("150000"),
            max_installments=3,
            due_day=5,
        )

        self.rent = Rent.objects.create(
            lease=self.lease,
            period=date(2026, 10, 1),
            amount_due=Decimal("75000"),
            due_date=date(2026, 10, 5),
        )

    # ---------------------------------------------------------
    # ÉTAT INITIAL
    # ---------------------------------------------------------

    def test_rent_exists(self):
        self.assertEqual(
            self.rent.amount_due,
            Decimal("75000"),
        )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("0"),
        )

        self.assertEqual(
            self.rent.remaining_amount,
            Decimal("75000"),
        )

        self.assertEqual(
            self.rent.installments_used,
            0,
        )

        self.assertEqual(
            self.rent.remaining_installments,
            3,
        )

        self.assertEqual(
            self.rent.status,
            Rent.Status.PENDING,
        )

    # ---------------------------------------------------------
    # PAIEMENT PARTIEL
    # ---------------------------------------------------------

    def test_create_partial_payment(self):
        payment = create_payment(
            rent=self.rent,
            amount=Decimal("20000"),
            payment_date=date(2026, 10, 1),
            payment_method="MOBILE_MONEY",
            reference="TEST-001",
        )

        self.assertEqual(
            payment.amount,
            Decimal("20000"),
        )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("20000"),
        )

        self.assertEqual(
            self.rent.remaining_amount,
            Decimal("55000"),
        )

        self.assertEqual(
            self.rent.installments_used,
            1,
        )

        self.assertEqual(
            self.rent.remaining_installments,
            2,
        )

        self.assertEqual(
            self.rent.status,
            Rent.Status.PARTIAL,
        )

    # ---------------------------------------------------------
    # REFUS D'UN PAIEMENT SUPÉRIEUR AU RESTE
    # ---------------------------------------------------------

    def test_reject_payment_above_remaining_amount(self):
        create_payment(
            rent=self.rent,
            amount=Decimal("20000"),
            payment_date=date(2026, 10, 1),
            payment_method="MOBILE_MONEY",
            reference="TEST-001",
        )

        with self.assertRaisesMessage(
            ValidationError,
            "Le montant du paiement dépasse le reste à payer.",
        ):
            create_payment(
                rent=self.rent,
                amount=Decimal("60000"),
                payment_date=date(2026, 10, 2),
                payment_method="MOBILE_MONEY",
                reference="TEST-002",
            )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("20000"),
        )

        self.assertEqual(
            self.rent.remaining_amount,
            Decimal("55000"),
        )

        self.assertEqual(
            self.rent.installments_used,
            1,
        )

    # ---------------------------------------------------------
    # DERNIÈRE TRANCHE
    # ---------------------------------------------------------

    def test_last_installment_must_match_remaining_amount(self):
        create_payment(
            rent=self.rent,
            amount=Decimal("20000"),
            payment_date=date(2026, 10, 1),
            payment_method="MOBILE_MONEY",
            reference="TEST-001",
        )

        create_payment(
            rent=self.rent,
            amount=Decimal("30000"),
            payment_date=date(2026, 10, 3),
            payment_method="MOBILE_MONEY",
            reference="TEST-002",
        )

        self.assertEqual(
            self.rent.remaining_amount,
            Decimal("25000"),
        )

        self.assertEqual(
            self.rent.remaining_installments,
            1,
        )

        with self.assertRaisesMessage(
            ValidationError,
            "La dernière tranche doit correspondre exactement au reste à payer.",
        ):
            create_payment(
                rent=self.rent,
                amount=Decimal("20000"),
                payment_date=date(2026, 10, 4),
                payment_method="MOBILE_MONEY",
                reference="TEST-003",
            )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("50000"),
        )

        self.assertEqual(
            self.rent.remaining_amount,
            Decimal("25000"),
        )

        self.assertEqual(
            self.rent.installments_used,
            2,
        )

        self.assertEqual(
            self.rent.remaining_installments,
            1,
        )

    # ---------------------------------------------------------
    # PAIEMENT COMPLET EN UNE SEULE FOIS
    # ---------------------------------------------------------

    def test_full_payment_in_one_installment(self):
        payment = create_payment(
            rent=self.rent,
            amount=Decimal("75000"),
            payment_date=date(2026, 10, 5),
            payment_method="MOBILE_MONEY",
            reference="TEST-FULL-001",
        )

        self.assertEqual(
            payment.amount,
            Decimal("75000"),
        )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("75000"),
        )

        self.assertEqual(
            self.rent.remaining_amount,
            Decimal("0"),
        )

        self.assertEqual(
            self.rent.installments_used,
            1,
        )

        self.assertEqual(
            self.rent.remaining_installments,
            2,
        )

        self.assertEqual(
            self.rent.status,
            Rent.Status.PAID,
        )

    # ---------------------------------------------------------
    # PAIEMENT COMPLET EN TROIS TRANCHES
    # ---------------------------------------------------------

    def test_full_payment_in_three_installments(self):
        create_payment(
            rent=self.rent,
            amount=Decimal("20000"),
            payment_date=date(2026, 10, 1),
            payment_method="MOBILE_MONEY",
            reference="TEST-001",
        )

        create_payment(
            rent=self.rent,
            amount=Decimal("30000"),
            payment_date=date(2026, 10, 3),
            payment_method="MOBILE_MONEY",
            reference="TEST-002",
        )

        create_payment(
            rent=self.rent,
            amount=Decimal("25000"),
            payment_date=date(2026, 10, 5),
            payment_method="MOBILE_MONEY",
            reference="TEST-003",
        )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("75000"),
        )

        self.assertEqual(
            self.rent.remaining_amount,
            Decimal("0"),
        )

        self.assertEqual(
            self.rent.installments_used,
            3,
        )

        self.assertEqual(
            self.rent.remaining_installments,
            0,
        )

        self.assertEqual(
            self.rent.status,
            Rent.Status.PAID,
        )

    # ---------------------------------------------------------
    # REFUS D'UN QUATRIÈME PAIEMENT
    # ---------------------------------------------------------

    def test_reject_payment_after_max_installments(self):
        create_payment(
            rent=self.rent,
            amount=Decimal("20000"),
            payment_date=date(2026, 10, 1),
            payment_method="MOBILE_MONEY",
            reference="TEST-001",
        )

        create_payment(
            rent=self.rent,
            amount=Decimal("30000"),
            payment_date=date(2026, 10, 3),
            payment_method="MOBILE_MONEY",
            reference="TEST-002",
        )

        create_payment(
            rent=self.rent,
            amount=Decimal("25000"),
            payment_date=date(2026, 10, 5),
            payment_method="MOBILE_MONEY",
            reference="TEST-003",
        )

        with self.assertRaisesMessage(
            ValidationError,
            "Ce loyer est déjà entièrement payé.",
        ):
            create_payment(
                rent=self.rent,
                amount=Decimal("1000"),
                payment_date=date(2026, 10, 6),
                payment_method="MOBILE_MONEY",
                reference="TEST-004",
            )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("75000"),
        )

        self.assertEqual(
            self.rent.installments_used,
            3,
        )

    # ---------------------------------------------------------
    # REFUS D'UN PAIEMENT SUR UN LOYER DÉJÀ PAYÉ
    # ---------------------------------------------------------

    def test_reject_payment_when_rent_already_paid(self):
        create_payment(
            rent=self.rent,
            amount=Decimal("75000"),
            payment_date=date(2026, 10, 5),
            payment_method="MOBILE_MONEY",
            reference="TEST-FULL-001",
        )

        with self.assertRaisesMessage(
            ValidationError,
            "Ce loyer est déjà entièrement payé.",
        ):
            create_payment(
                rent=self.rent,
                amount=Decimal("5000"),
                payment_date=date(2026, 10, 6),
                payment_method="MOBILE_MONEY",
                reference="TEST-FULL-002",
            )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("75000"),
        )

        self.assertEqual(
            self.rent.remaining_amount,
            Decimal("0"),
        )

    # ---------------------------------------------------------
    # REFUS D'UN MONTANT NÉGATIF
    # ---------------------------------------------------------

    def test_reject_negative_payment(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Le montant du paiement doit être supérieur à zéro.",
        ):
            create_payment(
                rent=self.rent,
                amount=Decimal("-1000"),
                payment_date=date(2026, 10, 1),
                payment_method="MOBILE_MONEY",
                reference="TEST-NEGATIVE",
            )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("0"),
        )

        self.assertEqual(
            self.rent.installments_used,
            0,
        )

    # ---------------------------------------------------------
    # REFUS D'UN PAIEMENT À ZÉRO
    # ---------------------------------------------------------

    def test_reject_zero_payment(self):
        with self.assertRaisesMessage(
            ValidationError,
            "Le montant du paiement doit être supérieur à zéro.",
        ):
            create_payment(
                rent=self.rent,
                amount=Decimal("0"),
                payment_date=date(2026, 10, 1),
                payment_method="MOBILE_MONEY",
                reference="TEST-ZERO",
            )

        self.assertEqual(
            self.rent.total_paid,
            Decimal("0"),
        )

        self.assertEqual(
            self.rent.installments_used,
            0,
        )
        
    def test_rent_status_late(self):
        with patch(
            "django.utils.timezone.localdate",
            return_value=date(2026, 10, 6),
        ):
            self.assertEqual(
                self.rent.status,
                Rent.Status.LATE,
            )
    
    def test_rent_is_not_late_on_due_date(self):
        with patch(
            "django.utils.timezone.localdate",
            return_value=date(2026, 10, 5),
        ):
            self.assertEqual(
                self.rent.status,
                Rent.Status.PENDING,
            )



from django.core.exceptions import ValidationError

from rest_framework import serializers

from payments.models import Payment
from payments.services import create_payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "rent",
            "amount",
            "payment_date",
            "payment_method",
            "reference",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        try:
            return create_payment(**validated_data)
        except ValidationError as exc:
            raise serializers.ValidationError(
                {"detail": exc.messages}
            ) from exc
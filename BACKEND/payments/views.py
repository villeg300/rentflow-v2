from rest_framework import generics

from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

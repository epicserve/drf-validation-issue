from rest_framework import viewsets

from pizzas.models import Pizza, Topping, ToppingType, Crust
from pizzas.serializers import PizzaSerializer, ToppingSerializer, ToppingTypeSerializer, CrustSerializer


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.prefetch_related('toppings').all()
    serializer_class = PizzaSerializer


class CrustViewSet(viewsets.ModelViewSet):
    queryset = Crust.objects.all()
    serializer_class = CrustSerializer


class ToppingTypeViewSet(viewsets.ModelViewSet):
    queryset = ToppingType.objects.all()
    serializer_class = ToppingTypeSerializer


class ToppingViewSet(viewsets.ModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer

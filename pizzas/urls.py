from django.urls import include, path

from rest_framework import routers

from pizzas import api

router = routers.DefaultRouter()
router.register(r'pizzas', api.PizzaViewSet)
router.register(r'crust', api.CrustViewSet)
router.register(r'toppings', api.ToppingViewSet)
router.register(r'topping-types', api.ToppingTypeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework import serializers

from pizzas.models import Pizza, Topping, ToppingType


class PizzaSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Pizza
        fields = ('url', 'name', 'price', 'toppings')

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price can't be less than zero.")
        return value

    def validate(self, data):

        # Require at least 1 sauce and cheese > 0
        sauce_num = 0
        cheese_num = 0
        for topping in data.get('toppings', []):
            if topping.type.slug == 'sauce':
                sauce_num += 1
            if topping.type.slug == 'cheese':
                cheese_num += 1

        topping_errors = []
        if sauce_num != 1:
            topping_errors.append("No sauce, please add some sauce.")

        if cheese_num < 1:
            topping_errors.append("No cheese, please add some cheese.")

        if topping_errors:
            raise serializers.ValidationError({'toppings': topping_errors})

        return data


class ToppingTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ToppingType
        fields = ('name', )


class ToppingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Topping
        fields = ('name', 'type')

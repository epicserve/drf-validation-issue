from django import forms

from pizzas.models import Pizza


class PizzaForm(forms.ModelForm):

    class Meta:
        model = Pizza
        fields = ('name', 'price', 'crust', 'toppings')

    def clean(self):

        price = self.cleaned_data.get('price')
        toppings = self.cleaned_data.get('toppings', [])

        if price and price < 0:
            self.add_error('price', "Price can't be less than zero.")

        # Require at least 1 sauce and cheese > 0
        sauce_num = 0
        cheese_num = 0
        for topping in toppings:
            if topping.type.slug == 'sauce':
                sauce_num += 1
            if topping.type.slug == 'cheese':
                cheese_num += 1

        topping_errors = []
        if sauce_num != 1:
            self.add_error('toppings', 'No sauce, please add some sauce.')

        if cheese_num < 1:
            self.add_error('toppings', 'No cheese, please add some cheese.')

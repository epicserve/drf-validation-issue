from django.core.management.base import BaseCommand, CommandError

from pizzas.models import Topping, ToppingType

cheese_list = [
    'Cheddar',
    'Colby',
    'Goat Cheese',
    'Monterey Jack',
    'Mozzarella',
    'Provolone',
]

sauce_list = [
    'Marinara',
    'Alfredo',
    'BBQ',
]

meat_list = [
    'Bacon',
    'BBQ Chicken',
    'Beef',
    'Cajun Chicken',
    'Chicken',
    'Ham',
    'Meatballs',
    'Pepperoni',
    'Proscuitto',
    'Salami',
    'Sausage',
    'Turkey',
]

sea_food_list = [
    'Anchovies',
    'Cajun Prawn',
    'Crayfish',
    'Lobster',
    'Oysters',
    'Prawns',
    'Salmon',
    'Shrimps',
    'Smoked Salmon',
    'Squid',
    'Tuna',
    'Whitebait',
]

vegetable_list = [
    'Black Beans',
    'Broccoli',
    'Carrot',
    'Green Peppers',
    'Lettuce',
    'Mushrooms',
    'Onions',
    'Olives',
    'Red Beans',
    'Red Onions',
    'Red Peppers',
    'Roasted Cauliflower',
    'Roasted Garlic',
    'Roasted Peppers',
    'Snow Peas',
    'Spinach',
    'Sun Dried Tomatoes',
    'Sweet Corn',
]

topping_types = [
    {'name': 'Cheese', 'slug': 'cheese', 'list': cheese_list},
    {'name': 'Sauce', 'slug': 'sauce', 'list': sauce_list},
    {'name': 'Meat', 'slug': 'meat', 'list': meat_list},
    {'name': 'Sea Food', 'slug': 'sea-food', 'list': sea_food_list},
    {'name': 'Vegetable', 'slug': 'vegetable', 'list': vegetable_list},
]


def add_toppings(topping_list, topping_type):
    for topping_name in topping_list:
        Topping.objects.create(name=topping_name, type=topping_type)


class Command(BaseCommand):
    help = 'Load initial pizza toppings'

    def handle(self, *args, **options):
        for topping in topping_types:
            add_toppings(topping['list'], ToppingType.objects.create(name=topping['name'], slug=topping['slug']))

        self.stdout.write(self.style.SUCCESS('Toppings loaded.'))

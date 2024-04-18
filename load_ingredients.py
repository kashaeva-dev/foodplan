from conf.wsgi import *

import json

from foodplan.models import Ingredient

ingredients = Ingredient.objects.all()

with open('products.json', 'r') as file:
    products = file.read()

products = json.loads(products)


if __name__ == '__main__':
    for product in products:
        name = product['name']
        bgu = product['bgu'].split(',')
        protein = float(bgu[0])
        fat = float(bgu[1])
        carbohydrate = float(bgu[2])
        energy = int(product['kcal'].split('.')[0])
        ingredient = Ingredient.objects.create(name=name,
                                               protein=protein,
                                               fat=fat,
                                               carbohydrate=carbohydrate,
                                               energy=energy
                                               )

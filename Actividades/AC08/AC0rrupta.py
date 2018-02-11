__author__ = {"lechodiman", "sfga"}
# -*- coding: utf-8 -*-
import random

###############################################################################
# Solo puedes escribir código aquí, cualquier modificación fuera de las lineas
# será penalizada con nota 1.0


class MetaPerson(type):
    def __new__(cls, name, bases, dic):
        if name == 'Chef':
            if Person not in bases:
                print("La clase no hereda de Person, lo arreglare")
                bases = (Person, )

            if 'cook' not in dic.keys():
                print('No tiene el metodo cook, lo voy a arreglar')

                def new_cook(self):
                    plate = Plate()
                    self.choose_food(plate)
                    self.choose_drink(plate)

                    return plate

                dic['cook'] = new_cook

            return super().__new__(cls, name, bases, dic)

        if name == 'Client':
            if Person not in bases:
                print("La clase no hereda de Person, lo arreglare")
                bases = (Person, )

            if 'eat' not in dic.keys():
                print('No tiene el metodo eat, lo voy a arreglar')

                def eat(self, plate):
                    error = False
                    if not isinstance(plate.food, Food):
                        print("Mi comida no es comida")
                        error = True
                    if not isinstance(plate.drink, Drink):
                        print("Mi bebida no es bebida")
                        error = True

                    if not error:
                        total_quality = (plate.food._quality + plate.drink._quality) / 2
                        if total_quality > 50:
                            print("Que delicia")
                        else:
                            print("Esto no es digno de mi paladar")

                dic['eat'] = eat
            return super().__new__(cls, name, bases, dic)

    def __call__(cls, *args, **kwargs):
        ob = super().__call__(*args, **kwargs)
        setattr(ob, 'restaurant', None)
        return ob


class MetaRestaurant(type):
    dict_restaurant = dict()

    def __new__(meta, name, bases, dic):

        def llega_cliente(self, clients):
            for client in clients:
                if not isinstance(client, Client):
                    print("Hay algo que no es cliente")
                else:
                    self.clients.append(client)

        def cliente_se_va(self, client_name):
            for client in self.clients:
                if client.name == client_name:
                    ob_client = client
                    break
            self.clients.remove(ob_client)

        def new_start(self, *args, **kwargs):
            if len(self.clients) == 0:
                print("{} no tiene clientes, que pena".format(self.name))
            else:
                print("{} comienza a funcionar".format(self.name))
                for i in range(1):  # Se hace el estudio por 5 dias
                    print("----- Día {} -----".format(i + 1))
                    plates = []
                    for chef in self.chefs:
                        for j in range(3):  # Cada chef cocina 3 platos
                            plates.append(chef.cook())  # Retorna platos de comida y bebida

                    for client in self.clients:
                        for plate in plates:
                            client.eat(plate)

        dic['llega_cliente'] = llega_cliente
        dic['cliente_se_va'] = cliente_se_va
        dic['start'] = new_start

        return super().__new__(meta, name, bases, dic)

    def __call__(cls, *args, **kwargs):
        restaurant_name = args[0]
        if len(args) == 1:
            args = list(args)
            args.append([])
            args.append([])
            return super().__call__(*args, **kwargs)
        restaurant_chefs = args[1]

        for chef in restaurant_chefs:
            if chef.restaurant is not None:
                ob_restaurant = MetaRestaurant.dict_restaurant[chef.restaurant]
                cant_chefs = len(ob_restaurant.chefs)
                if cant_chefs == 1:
                    print('Instanciacion denegada')
                    return None
        for chef in restaurant_chefs:
            if chef.restaurant is not None:
                ob_restaurant = MetaRestaurant.dict_restaurant[chef.restaurant]
                ob_restaurant.chefs.remove(chef)
            chef.restaurant = restaurant_name

        if len(args) == 2:
            args = list(args)
            args.append([])
        new_restaurant = super().__call__(*args, **kwargs)

        print("Instanciacion de restaurant exitosa")
        print("Se han contratado los siguientes chefs: ")
        for chef in restaurant_chefs:
            print(chef.name)
        MetaRestaurant.dict_restaurant[new_restaurant.name] = new_restaurant
        return super().__call__(*args, **kwargs)

###############################################################################
# De aquí para abajo no puedes cambiar ABSOLUTAMENTE NADA


class Person:
    def __init__(self, name):
        self.name = name


class Food:
    def __init__(self, ingredients):
        self._quality = random.randint(50, 200)
        self.preparation_time = 0
        self.ingredients = ingredients

    @property
    def quality(self):
        return self._quality * random.random()


class Drink:
    def __init__(self):
        self._quality = random.randint(5, 15)

    @property
    def quality(self):
        return self._quality * random.random()


class Restaurant(metaclass=MetaRestaurant):
    def __init__(self, name, chefs, clients):
        self.name = name
        self.chefs = chefs
        self.clients = clients

    def start(self):
        for i in range(1):  # Se hace el estudio por 5 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook())  # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)


class Pizza(Food):
    def __init__(self, ingredients):
        super(Pizza, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 100)


class Salad(Food):
    def __init__(self, ingredients):
        super(Salad, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 60)


class Coke(Drink):
    def __init__(self):
        super(Coke, self).__init__()
        self._quality -= 5


class Juice(Drink):
    def __init__(self):
        super(Juice, self).__init__()
        self._quality += 5


class Plate:
    def __init__(self):
        self.food = None
        self.drink = None


class Chef(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Chef, self).__init__(name)

    def choose_food(self, plate):
        food_choice = random.randint(0, 1)
        ingredients = []
        if food_choice == 0:
            for i in range(3):
                ingredients.append(random.choice(["pepperoni", "piña", "cebolla", "tomate", "jamón", "pollo"]))
            plate.food = Pizza(ingredients)
        else:
            for i in range(2):
                ingredients.append(random.choice(["crutones", "espinaca", "manzana", "zanahoria", "palta"]))
            plate.food = Salad(ingredients)

    def choose_drink(self, plate):
        drink_choice = random.randint(0, 1)
        if drink_choice == 0:
            plate.drink = Coke()
        else:
            plate.drink = Juice()


class Client(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Client, self).__init__(name)


if __name__ == '__main__':

    chefs = [Chef("Enzo"), Chef("Nacho"), Chef("Diego")]
    clients = [Client("Bastian"), Client("Flori"),
               Client("Rodolfo"), Client("Felipe")]
    McDollars = Restaurant("Mc", chefs, clients)

    BurgerPimp = Restaurant("BK")

    KFK = Restaurant("KFK", [Chef("Enzo")])

    McDollars.start()
    KFK.start()

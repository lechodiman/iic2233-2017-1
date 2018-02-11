__author__ = "cotehidalgov"

#Herencia
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import random

class Plate:
	def __init__(self, food, drink):
		self.food = food
		self.drink = drink

class Food(metaclass = ABCMeta):
	def __init__(self, ingredients):
		self.calidad = random.randint(50,200)
		self.ingredients = ingredients
		self.tiempo = 0


	def check_time(self): 
		if self.tiempo >= 30:
			self.calidad -= 30


class Pizza(Food):
	def __init__(self, ingredients):
		super().__init__(ingredients)
		self.ingredients.append("base de queso")
		self.ingredients.append("salsa de tomate")
		self.tiempo = random.randint(20,100)

	def check_ingredients(self):
		if "peperoni" in self.ingredients:
			self.calidad +=50
		if "pina" in self.ingredients:
			self.calidad -= 50


class Salad(Food):
	def __init__(self, ingredients):
		super().__init__(ingredients)
		self.ingredients.append("base de lechuga")
		self.tiempo = random.randint(5,60)

	def check_ingredients(self):
		if "crutones" in self.ingredients:
			self.calidad += 20
		if "manzana" in self.ingredients:
			self.calidad -=20

class Drink(metaclass = ABCMeta):
	def __init__(self):
		self.calidad = random.randint(50,200)

class Juice(Drink):
	def __init__(self):
		super().__init__()
		self.calidad += 30

class Soda(Drink):
	def __init__(self):
		super().__init__()
		self.calidad -= 30

class Personality(metaclass = ABCMeta):
	personality = None
	def react(self,quality):
		if quality >= 100:
			self.im_happy()
		else:
			self.im_mad()

	def im_happy(self):
		pass

	def im_mad(self):
		pass

		
class Cool(Personality):
	def im_happy(self):
		print("Yumi! Que rico")

	def im_mad(self):
		print("Preguntare si puedo cambiar de plato")


class Hater(Personality):
	def im_happy(self):
		print("No esta malo, pero igual prefiero Pizza x2")

	def im_mad(self):
		print("Nunca mas vendre a Daddy Juan's")

class Person(metaclass = ABCMeta): # Solo los clientes tienen personalidad en esta actividad
	def __init__(self, name):
		self.name = name

class Chef(Person):
	def __init__(self, nombre):
		super().__init__(nombre)
	
	def cook(self):
		lista_ing = ["pepperoni", "pina", "cebolla", "tomate", "jamon", "pollo"]
		ing_pizza_1 = random.choice(lista_ing)
		ing_pizza_2 = random.choice(lista_ing)
		ing_pizza_3 = random.choice(lista_ing)

		lista_salad = ["crutones", "espinaca", "manzana", "zanahoria"]
		ing_salad_1 = random.choice(lista_salad)
		ing_salad_2 = random.choice(lista_salad)

		pizza_salad_choice = random.choice(["pizza", "salad"])
		soda_juice_choice = random.choice(["soda", "juice"])

		if pizza_salad_choice =="pizza":
			f = Pizza([ing_pizza_1, ing_pizza_2, ing_pizza_3])
		elif pizza_salad_choice == "salad":
			f = Salad([ing_salad_1, ing_salad_2])

		if soda_juice_choice == "soda":
			d = Soda()
		elif soda_juice_choice == "juice":
			d = Juice()

		return Plate(f, d)



class Client(Person):
	def __init__(self, name, personality):
		super().__init__(name)
		self.personality = personality

	def eat(self, plate):
		calidad_final = (plate.food.calidad + plate.drink.calidad)/2
		self.personality.react(calidad_final)


class Restaurant:
	def __init__(self, chefs, clients):
		self.chefs = chefs
		self.clients = clients

	def start(self):
		for i in range(3): # Se hace el estudio por 3 dias
			print("----- Día {} -----".format(i + 1))
			plates = []
			for chef in self.chefs: 
				for j in range(3):  # Cada chef cocina 3 platos
					plates.append(chef.cook()) # Retorna platos de comida y bebida

			for client in self.clients:
				for plate in plates:
					client.eat(plate)



if __name__ == '__main__':
	chefs = [Chef("Cote"), Chef("Joaquin"), Chef("Andres")]
	clients = [Client("Bastian", Hater()), Client("Flori", Cool()), 
				Client("Antonio", Hater()), Client("Felipe", Cool())]

	restaurant = Restaurant(chefs, clients)
	restaurant.start()






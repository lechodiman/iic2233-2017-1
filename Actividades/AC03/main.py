__author__ = 'Luis Chodiman' \
             'Ricardo Del Rio'

from camion_producto import Camion, Producto
from centro_acopio import CentroAcopio
from collections import deque


def cargar_camiones():
    with open("camiones.txt", "r") as rf:
        lista_camiones = []
        for line in rf:
            linea_sin_espacios = line.strip().split(",")
            cap_max = linea_sin_espacios[0]
            urgencia = linea_sin_espacios[1]
            camion = Camion(cap_max, urgencia)

            lista_camiones.append(camion)

        return lista_camiones


def cargar_productos():
    with open("productos.txt", "r") as rf:
        lista_productos = []
        for line in rf:
            linea_sin_espacios = line.strip().split(",")
            nombre = linea_sin_espacios[1]
            tipo = linea_sin_espacios[0]
            peso = linea_sin_espacios[2]

            producto = Producto(nombre, tipo, peso)

            lista_productos.append(producto)

        return lista_productos

lista_camiones = cargar_camiones()
lista_productos = cargar_productos()
centro_de_acopio = CentroAcopio()

for camion in lista_camiones:
    centro_de_acopio.recibir_camion(camion)

centro_de_acopio.recibir_donacion(lista_productos)

for i in range(0, 5):
    centro_de_acopio.rellenar_camion()
    centro_de_acopio.enviar_camion()

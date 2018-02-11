from collections import deque


class CentroAcopio:

    def __init__(self):
        self.fila = deque()
        self.pila_bodega = dict()

    def recibir_donacion(self, lista):

        donaciones_entrantes = lista

        while len(donaciones_entrantes) != 0:
            donacion = donaciones_entrantes.pop()

            if donacion.tipo not in self.pila_bodega:
                self.pila_bodega[donacion.tipo] = []

            pila = self.pila_bodega[donacion.tipo]
            pila.append(donacion)

    def recibir_camion(self, camion):
        if len(self.fila) == 0:
            self.fila.append(camion)
        else:
            urg_camion_agregar = camion.urgencia
            for i in range(len(self.fila))[::-1]:
                u = self.fila[i].urgencia
                if u <= urg_camion_agregar:
                    indice_a_agregar = i
            try:
                self.fila.insert(indice_a_agregar, camion)
            except:
                self.fila.append(camion)

    def enviar_camion(self):
        primer_camion = self.fila[0]
        if primer_camion.esta_lleno:
            self.fila.popleft()
            print("El envio del camion fue exitoso")

    def rellenar_camion(self):
        primer_camion = self.fila[0]
        productos_sin_ordenar = []
        for k, pila in self.pila_bodega.items():
            for producto in pila:
                productos_sin_ordenar.append(producto)

        productos_sin_ordenar.sort(reverse=True)

        for producto in productos_sin_ordenar:
            if int(producto.peso) <= primer_camion.agregar_producto():
                primer_camion.agregar_producto(producto)

    def profuctos_por_tipo(self, tipo):
        if tipo not in self.pila_bodega:
            print("No hay productos de tipo: {}".format(tipo))
        else:
            print("Productos de tipo: {}".format(tipo))
            for product in self.pila_bodega[tipo]:
                print(product)

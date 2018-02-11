__author__ = 'Luis Chodiman' \
             'Ricardo Del Rio'


class Camion():

    def __init__(self, capacidad_maxima, urgencia):
        self.capacidad_maxima = int(capacidad_maxima)
        self.urgencia = urgencia
        self.productos = dict()
        self.esta_lleno = False
        self.llenado = 0

    def agregar_producto(self, producto=None):

        if producto != None:
            if self.llenado + producto.peso <= self.capacidad_maxima:
                self.llenado += producto.peso
                if producto.tipo in self.productos:
                    self.productos[producto.tipo] += 1
                else:
                    self.productos = 1

        return int(self.capacidad_maxima) - int(self.llenado)


#cant_diponible = camion.agregar_producto(producto)

    def __str__(self):
        texto = 'TIPO / CANTIDAD'
        for i in self.poductos:
            texto += '\n' + i + ' / ' + str(self.productos[i])

        return texto


class Producto():

    def __init__(self, nombre, tipo, peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = int(peso)

    #def __eq__(self, other):
    #    return (self.nombre == other.nombre) and (self.tipo == other.tipo)

    def __lt__(self, other):
        return self.peso < other.peso

    def __str__(self):
        return 'Nombre: ' + nombre + '\nTipo: ' + tipo + '\nPeso: ' + str(peso)

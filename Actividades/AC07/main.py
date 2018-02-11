__author__ = 'lechodiman'

import random
from datetime import datetime


"""
Escriba sus decoradores y funciones auxiliares en este espacio.
"""


def verificar_transferencia(original_function):
    def transferencia(self, origen, destino, monto, clave):
        # Verifico que existan
        if origen not in self.cuentas:
            print("No esta la cuenta origen")
            raise AssertionError
        if destino not in self.cuentas:
            print("No esta la cuenta destino")
            raise AssertionError

        cuenta_1 = self.cuentas[origen]

        # Verifico que hay suficiente dinero en la cuenta de origen
        if cuenta_1.saldo < monto:
            print("No hay suficiente dinero en la cuenta de origen")
            raise AssertionError

        if cuenta_1.clave != clave:
            print("La clave ingresada es incorrecta")
            raise AssertionError

        return original_function(self, origen, destino, monto, clave)

    return transferencia


def verificar_inversion(original_function):
    def inversion(self, cuenta, monto, clave):
        if cuenta not in self.cuentas:
            print("No esta la cuenta origen")
            raise AssertionError

        cuenta_1 = self.cuentas[cuenta]

        if monto > cuenta_1.saldo:
            print("No hay saldo suficiente para invertir")
            raise AssertionError

        if clave != cuenta_1.clave:
            print("La clave ingresada es incorrecta")
            raise AssertionError

        new_inversiones = cuenta_1.inversiones + monto

        if new_inversiones > 10000000:
            print("Al hacer esta inversion se sobrepasa el maximo permitido")
            raise AssertionError

        return original_function(self, cuenta, monto, clave)
    return inversion


def verificar_cuenta(original_function):
    def creacion_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        if numero in self.cuentas:
            print("El numero de cuenta ya existe, se creara uno aleatorio")
            numero = self.crear_numero()

        if len(clave) != 4:
            print("La clave debe tener exactamente 4 numeros")
            raise AssertionError

        if rut.count("-") != 1:
            print("Hay mas de un gion en el rut")
            raise AssertionError

        before_guion, after_guion = rut.split("-")

        if not before_guion.isnumeric() or not after_guion.isnumeric():
            print("Hay elementos que no son numeros")
            raise AssertionError

        print("Cuenta creada correctamente")
        return original_function(self, nombre, rut, clave, numero, saldo_inicial)

    return creacion_cuenta


def verificar_saldo(original_function):
    def imprimir_saldo(self, numero_cuenta):
        if numero_cuenta not in self.cuentas:
            print("No existe la cuenta")
            raise AssertionError

        result = original_function(self, numero_cuenta)
        new_result = result / 5

        return new_result

    return imprimir_saldo


def path_decorator(path):
    def log(original_function):
        def wrapper(*args, **kwargs):
            time_date = datetime.now()
            action_name = original_function.__name__

            file_name = path

            with open(file_name, "a") as af:
                line = "{0} - {1}: {2}, {3} |".format(time_date, action_name, args[1:], kwargs)
                af.write(line + "\n")

            return original_function(*args, **kwargs)
        return wrapper
    return log

"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las 
funciones/clases.
"""


class Banco:
    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()

    @path_decorator('test.txt')
    @verificar_saldo
    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5

    @path_decorator('test.txt')
    @verificar_transferencia
    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto

    @path_decorator('test.txt')
    @verificar_cuenta
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta

    @path_decorator('test.txt')
    @verificar_inversion
    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:
    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


bco = Banco("Santander")
bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
# bco.crear_cuenta("Juan", "19231233--3", "1234", bco.crear_numero())

# print(repr(bco))
# print()
'''
if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    # bco.crear_cuenta("Juan", "19231233--3", "1234", bco.crear_numero())

    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar 
    las pruebas que estime necesaria para comprobar el funcionamiento de su 
    solucion.
    """
    try:
        print(bco.saldo(10))
    except AssertionError as error:
        print('Error: ', error)

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    try:
        bco.transferir(1, 2, 5000, "4321")
    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    try:
        bco.invertir(2, 200000, "1234")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    try:
        bco.invertir(2, 200000, "4321")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))
'''


class ArgumentoInvalido(Exception):

    def __str__(self):
        return 'CAUSA: Argumento Invalido'


class ReferenciaInvalida(Exception):

    def __str__(self):
        return 'CAUSA: Referencia Invalida'


class ErrorDeTipo(Exception):

    def __str__(self):
        return 'CAUSA: Error de Tipo'


class ErrorMatematico(Exception):

    def __str__(self):
        return 'CAUSA: Error Matematico'


class ImposibleProcesar(Exception):

    def __str__(self):
        return 'CAUSA: Imposible Procesar'

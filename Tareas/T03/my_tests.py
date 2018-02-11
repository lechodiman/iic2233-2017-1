from basic_commands import generate_distribution, graficar
from commands_data_return import get_column, filtrar, operar, evaluar,\
    LEN, PROM, DESV, VAR, MEDIAN, comparar_columna, comparar
from consult_processing import asignar
import my_exceptions
import unittest


class AwesomeWindow:
    '''Class to simulate the window class in the actual interface'''
    pass


class SuperThing:
    pass


class MyTest(unittest.TestCase):

    def setUp(self):
        self.window = AwesomeWindow()

    def test_prom(self):
        self.assertEqual(PROM([1, 1, 2, 2], self.window), 1.5)
        with self.assertRaises(my_exceptions.ErrorDeTipo):
            PROM(5, self.window)
        self.assertRaises(my_exceptions.ReferenciaInvalida, PROM, 'x', self.window)
        self.window.x = (i for i in [1, 1])
        self.assertEqual(PROM('x', self.window), 1)
        delattr(self.window, 'x')

    def test_len(self):
        self.assertEqual(LEN([1, 1, 2, 2], self.window), 4)
        with self.assertRaises(my_exceptions.ErrorDeTipo):
            LEN(5, self.window)
        with self.assertRaises(my_exceptions.ReferenciaInvalida):
            LEN('x', self.window)
        self.window.x = (i for i in [1, 1])
        self.assertEqual(LEN('x', self.window), 2)
        delattr(self.window, 'x')

    def test_desv(self):
        self.assertEqual(DESV([1, 1, 2, 2], self.window), 0.5)
        with self.assertRaises(my_exceptions.ErrorDeTipo):
            DESV(5, self.window)
        with self.assertRaises(my_exceptions.ReferenciaInvalida):
            DESV('x', self.window)
        self.window.x = (i for i in [1, 1])
        self.assertEqual(DESV('x', self.window), 0)
        delattr(self.window, 'x')

    def test_median(self):
        self.assertEqual(MEDIAN([1, 1, 2, 2], self.window), 1.5)
        self.assertEqual(MEDIAN([1, 1, 2, 2, 2], self.window), 2)
        with self.assertRaises(my_exceptions.ErrorDeTipo):
            MEDIAN(5, self.window)
        with self.assertRaises(my_exceptions.ReferenciaInvalida):
            MEDIAN('x', self.window)
        with self.assertRaises(my_exceptions.ImposibleProcesar):
            MEDIAN([], self.window)
        self.window.x = (i for i in [1, 1])
        self.assertEqual(MEDIAN('x', self.window), 1.0)
        delattr(self.window, 'x')

    def test_var(self):
        self.assertEqual(VAR([1, 1, 2, 2], self.window), 0.25)
        with self.assertRaises(my_exceptions.ErrorDeTipo):
            VAR(5, self.window)
        with self.assertRaises(my_exceptions.ReferenciaInvalida):
            VAR('x', self.window)
        self.window.x = (i for i in [1, 1])
        self.assertEqual(VAR('x', self.window), 0)
        delattr(self.window, 'x')

    def test_asignar(self):
        s = SuperThing()
        asignar('x', s, self.window)
        self.assertEqual(getattr(self.window, 'x'), s)
        with self.assertRaises(my_exceptions.ImposibleProcesar):
            asignar('VAR', s, self.window)
        delattr(self.window, 'x')

    def test_filtrar(self):
        self.assertEqual(list(filtrar([1, 1, 2, 2], '>', 1, self.window)), [2, 2])
        with self.assertRaises(my_exceptions.ReferenciaInvalida):
            print(list(filtrar('y', '>', 2, self.window)))
        self.window.x = (i for i in [1, 1])
        self.assertEqual(list(filtrar('x', '>', 1, self.window)), [])
        delattr(self.window, 'x')

    def test_evaluar(self):
        def f(x):
            return x**2

        self.assertEqual(list(evaluar(f, 0, 5, 1, self.window)), [0.0, 1.0, 4.0, 9.0, 16.0])
        with self.assertRaises(my_exceptions.ReferenciaInvalida):
            print(list(evaluar('function_normal', 0, 5, 1, self.window)))
        self.window.function_normal = f
        self.assertEqual(list(evaluar('function_normal', 0, 2, 1, self.window)), [0.0, 1.0])
        delattr(self.window, 'function_normal')

    def test_comparar_columna(self):
        self.assertEqual(comparar_columna([1, 2], '>', 'PROM', [2, 3], self.window), False)
        with self.assertRaises(my_exceptions.ArgumentoInvalido):
            comparar_columna([1, 2], '>', 'super_average', [2, 3], self.window)

    def test_error_matematico(self):
        with self.assertRaises(my_exceptions.ErrorMatematico):
            function_normal = generate_distribution('NORMAL', 0, 0, self.window)
            function_normal(5)
        with self.assertRaises(my_exceptions.ErrorMatematico):
            function_gamma = generate_distribution('GAMMA', -1, 1, self.window)
            function_gamma(5)

    def test_error_argumento_invalido(self):
        with self.assertRaises(my_exceptions.ArgumentoInvalido):
            function_normal = generate_distribution('NORMAL', 0, 1, self.window, 'i am an extra arg')
            function_normal(5)


suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
unittest.TextTestRunner().run(suite)

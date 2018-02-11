import unittest
from main import Descifrador
import random


class TestearFormato(unittest.TestCase):
    def setUp(self):
        self.archivo = open("mensaje_marciano.txt")
        self.lines = self.archivo.readlines()
        self.lineas_sin_espacios = [line.strip() for line in self.lines]
        self.caracteres = []
        for linea in self.lineas_sin_espacios:
            for char in linea:
                if char != ' ':
                    self.caracteres.append(char)

    def tearDown(self):
        self.archivo.close()

    def test_archivo(self):
        self.assertEqual(len(self.caracteres), 408)
        self.assertEqual(sum(self.caracteres), 253)


class TestearMensaje(unittest.TestCase):
    def setUp(self):
        self.des = Descifrador('mensaje_marciano.txt')
        self.codigo = self.des.lectura_archivo()
        self.codigo = self.des.elimina_incorrectos()
        self.lista = self.des.cambiar_binario(self.des.codigo)
        self.texto = self.des.limpiador(self.lista)

    def test_incorrectos(self):
        codes = self.codigo.split(" ")
        self.assertNotEqual(len(random.choice(codes)), 5)
        self.assertNotEqual(len(random.choice(codes)), 8)

    def test_caracteres(self):
        self.assertEqual(self.texto, "https://www.youtube.com/watch?v=OWodAv1KHaM")

    def test_codificacion(self):
        code = self.codigo.split(" ")
        random_chunk = random.choice(code)
        random_char = random.choice(random_chunk.split(""))
        self.assertEqual(random_char, "1" or "0")

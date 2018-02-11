class CustomException(Exception):
    def __init__(self, lista):
        super().__init__("Hay una 'a' dentro del codigo")
        self.lista = lista

    def voltear_chunks(self):
        codigo = ''
        i_con_a = len(self.lista) + 1
        for i in range(len(self.lista)):
            if self.lista[i].find('a') != -1:
                chunk = self.lista[i][1::]
                codigo += ' ' + str(chunk[::-1])
                i_con_a = i
            elif i > i_con_a:
                codigo += ' ' + str(self.lista[i][::-1])
            elif i <= i_con_a:
                if len(self.lista[i]) < 6 or len(self.lista[i]) > 7:
                    pass
                else:
                    codigo += ' ' + str(self.lista[i])

        return codigo[1:]


class Descifrador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.suma = 0
        with open(self.nombre, "r") as self.archivo:
            lineas = self.archivo.readlines()
            self.codigo = ''
            self.texto = "".join(lineas).replace('\n', '')
            i = 0

    def lectura_archivo(self):
        with open(self.nombre, "r") as archivo:
            lineas = archivo.readlines()
            self.codigo = ''
            texto = "".join(lineas).replace('\n', '')
            for caracter in texto:
                self.codigo += caracter
            return self.codigo

    def elimina_incorrectos(self):
        lista = self.codigo.split(" ")
        self.codigo = ''
        try:
            raise CustomException(lista)

            for i in lista:
                if len(i) < 6 or len(i) > 7:
                    pass
                else:
                    self.codigo += ' ' + i
        except CustomException as err:
            code = err.voltear_chunks()
            self.codigo += ' ' + str(code)

        return self.codigo

    def cambiar_binario(self, binario):
        lista = binario.split(' ')
        texto = []
        for x in lista[1:]:
            texto.append(chr(int(x, 2)))
        return texto

    def limpiador(self, lista):
        i = -1
        string = ''
        try:
            while i < len(lista):
                i += 1
                if '$' != lista[i]:
                    string += lista[i]

        except IndexError:
            while i < len(lista):
                if '$' != lista[i]:
                    string += lista[i]
                i += 1

        return string

if __name__ == "__main__":
    try:
        des = Descifrador('mensaje_marciano.txt')
        codigo = des.lectura_archivo()
        codigo = des.elimina_incorrectos()
        try:
            lista = des.cambiar_binarios(des.codigo)
        except AttributeError as err:
            print("[ERROR] ", str(err))
            print("El atributo no existe")
        finally:
            print("Se inciara el atributo correcto")
            lista = des.cambiar_binario(des.codigo)
        texto = des.limpiador(lista)
        print(texto)
    except Exception as err:
        print('Esto no debiese imprimirse')


# des = Descifrador('mensaje_marciano.txt')
# codigo = des.lectura_archivo()
# codigo = des.elimina_incorrectos()
# print(codigo)
# lista = des.cambiar_binario(des.codigo)
# texto = des.limpiador(lista)
# print(texto)

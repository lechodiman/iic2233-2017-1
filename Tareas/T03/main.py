from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
from consult_processing import unit_process_consult
from my_exceptions import ReferenciaInvalida, ErrorDeTipo, ErrorMatematico, ArgumentoInvalido, ImposibleProcesar


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()

    def process_consult(self, querry_array):
        # Agrega en pantalla la solución. Muestra los graficos!!
        print(querry_array)
        for i, j in enumerate(querry_array):
            out = 'Probando funcion\nConsulta {}\n'.format(i)
            try:
                out += str(unit_process_consult(j, self))
            except (ArgumentoInvalido, ReferenciaInvalida, ErrorDeTipo, ErrorMatematico, ImposibleProcesar) as err:
                out += str(err) + "\n"
                out += 'ERROR: {}'.format(j) + "\n"
            finally:
                self.add_answer(out)

    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        print(querry_array)
        with open('resultados.txt', 'w') as wf:
            for i, q in enumerate(querry_array):
                output = '----Consulta {}----\n'.format(i)
                try:
                    output += str(unit_process_consult(q, self))
                except (ArgumentoInvalido, ReferenciaInvalida, ErrorDeTipo, ErrorMatematico, ImposibleProcesar) as err:
                    output += str(err) + "\n"
                    output += 'ERROR: {}'.format(q) + "\n"
                finally:
                    wf.write(output)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())

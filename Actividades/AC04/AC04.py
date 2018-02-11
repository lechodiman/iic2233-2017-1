# PRIMERA PARTE: Estructura basica


class Node:

    def __init__(self, d, n=None):
        self.data = d
        self.next_node = n

    def get_next(self):
        return self.next_node

    def set_next(self, n):
        self.next_node = n

    def get_data(self):
        return self.data

    def set_data(self, d):
        self.data = d


class LinkedList:

    def __init__(self, r=None):
        self.root = r
        self.size = 0

    def get_size(self):
        return self.size

    def add(self, d):
        new_node = Node(d, self.root)
        self.root = new_node
        self.size += 1

    def remove(self, d):
        this_node = self.root
        prev_node = None
        while this_node:
            if this_node.get_data() == d:
                if prev_node:
                    prev_node.set_next(this_node.get_next())
                else:
                    self.root = this_node
                self.size -= 1
                return True
            else:
                prev_node = this_node
                this_node = this_node.get_next()
        return False

    def find(self, d):
        this_node = self.root
        while this_node:
            if this_node.get_data() == d:
                return d
            else:
                this_node = this_node.get_next()
        return None

    def __repr__(self):
        rep = ''
        nodo_actual = self.root

        while nodo_actual:
            rep += '{0}->'.format(nodo_actual.data)
            nodo_actual = nodo_actual.next_node

        return rep

    def find_name(self, d):
        this_node = self.root
        while this_node:
            if this_node.get_data().nombre == d:
                return this_node.get_data()
            else:
                this_node = this_node.get_next()
        return None


# SEGUNDA PARTE: Clase Isla
class Isla:

    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = LinkedList()
        self.origenes = LinkedList()
        self.destinos = LinkedList()

    def __repr__(self):
        return str(self.nombre)


# TERCERA PARTE: Clase Archipielago
class Archipielago:

    def __init__(self, nombre_archivo):
    	self.nombre = nombre_archivo
    	self.islas = LinkedList()
    	self.nombres = LinkedList()

    def __repr__(self):
        isla_actual = self.islas.root
        msg = ""
        while isla_actual:

        	msg += "{} esta conectada con: {}".format(isla_actual.get_data().nombre,
        		isla_actual.get_data().destinos)
        

        	isla_actual = isla_actual.get_next()

        return msg


    def agregar_isla(self, nombre):
        isla = Isla(nombre)
        if self.nombres.find(nombre) == None:
            self.islas.add(isla)
            self.nombres.add(nombre)

    def conectadas(self, nombre_origen, nombre_destino):
        pass

    def agregar_conexion(self, nombre_origen, nombre_destino):

        if self.nombres.find(nombre_origen) == None and self.nombres.find(nombre_destino) == None:

            isla_1 = Isla(nombre_origen)
            isla_2 = Isla(nombre_destino)

            isla_1.destinos.add(isla_2)
            isla_2.origenes.add(isla_1)
            self.islas.add(isla_1)
            self.islas.add(isla_2)
            self.nombres.add(nombre_origen)
            self.nombres.add(nombre_destino)

        elif self.nombres.find(nombre_origen) != None and self.nombres.find(nombre_destino) == None:

            isla_2 = Isla(nombre_destino)
            isla_1 = self.islas.find_name(nombre_origen)

            isla_1.destinos.add(isla_2)
            isla_2.origenes.add(isla_1)

            self.islas.add(isla_2)
            self.nombres.add(nombre_destino)

        elif self.nombres.find(nombre_origen) != None and self.nombres.find(nombre_destino) != None:

            isla_1 = self.islas.find_name(nombre_origen)
            isla_2 = self.islas.find_name(nombre_destino)

            isla_1.destinos.add(isla_2)
            isla_2.origenes.add(isla_1)

        elif self.nombres.find(nombre_origen) == None and self.nombres.find(nombre_destino) != None:

        	isla_1 = Isla(nombre_origen)
       		isla_2 = self.islas.find_name(nombre_destino)

        	isla_1.destinos.add(isla_2)
        	isla_2.origenes.add(isla_1)

        	self.islas.add(isla_1)
        	self.nombres.add(nombre_origen)


    def construir(self, archivo):
    	with open(archivo, 'r') as rf:
    		for line in rf:
    			self.agregar_conexion(line.split(",")[0], line.split(",")[1])

        
    def propagacion(self, nombre_origen):
        isla_madre = self.islas.find_name(nombre_origen)

        lista_destinos = isla_madre.destinos

        lista_final = LinkedList()

        def buscar_destino(isla, lista_final):
	        destino_actual = isla.destinos.root
	        while destino_actual != None:
	        	#print('hola')
	        	if lista_final.find(destino_actual.get_data()) == None:
	        		lista_final.add(destino_actual.get_data())
	        		#print(type(destino_actual.get_data()))
	        		buscar_destino(destino_actual.get_data(), lista_final)
	        		print(lista_final)

	        	else:
	        		pass

	        	destino_actual = destino_actual.get_next()

        buscar_destino(isla_madre, lista_final)
        


        return lista_final

    def propagacion_2(self, lista_final):
    	isla_actual = lista_final.root

    	while isla_actual:
    		self.propagacion(isla_actual.get_data().nombre)

    		isla_actual = isla_actual.get_next()












# isla_1 = Isla("pepito")
# isla_2 = Isla("pepito2")
# lista = LinkedList()
# lista.add(isla_1)
# lista.add(isla_2)
# print(lista.find_name("pepito"))


if __name__ == '__main__':
    # No modificar desde esta linea
    # (puedes comentar lo que no este funcionando aun)
    arch = Archipielago("mapa.txt")
    arch.construir("mapa.txt")  # Instancia y construye
    #print(arch)  # Imprime el Archipielago de una forma que se pueda entender
    print(arch.propagacion("Perresus"))
    #print(arch.propagacion("Pasesterot"))
    #print(arch.propagacion("Cartonat"))
    #print(arch.propagacion("Womeston"))

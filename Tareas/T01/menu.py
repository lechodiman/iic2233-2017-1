from classes import (Incendio, Recurso, Meteorologia, Usuario, UsuarioANAF, Jefe, Piloto, MiFecha,
	leer_db, leer_db_usuarios)
from functions import is_bisiesto

def first_menu():

	print("*"*20)
	nombre_user = str(input("Ingrese Usuario: ")).strip()
	password = str(input("Ingrese Contrasena: ")).strip()
	users_db = leer_db_usuarios()
	match = False

	for user in users_db:
		nombre = str(user.nombre)
		contrasena = str(user.contrasena)
		if nombre == nombre_user and contrasena == password:
			match = True
			break

	if match:
		print("Bienvenido {}".format(user))
	else:
		print("Datos incorrectos")

	return (not match, user, password)

def hora():

	print("A continuacion seleccione una hora valida en formato hh: mm: ss \n")
	try:
		time = input("Hora: ")
		horas = int(time.strip().split(":")[0])
		minutos = int(time.strip().split(":")[1])
		segundos = int(time.strip().split(":")[2])
	except ValueError:
		print("Formato de hora invalido")
		return True, 0, 0, 0
	except IndexError:
		print("Formato de hora invalido")
		return True, 0, 0, 0

	error = False
	if horas < 0 or horas > 24:
		print("Rango de hora invalido")
		error = True
	if minutos < 0 or minutos > 60:
		print("Rango de minutos invalido")
		error = True
	if segundos < 0 or segundos > 60:
		print("Rango de segundos invalido")
		error = True

	return (error, horas, minutos, segundos)


def fecha():

	print("A continuacion seleccione una fecha valida en formato aaaa: mm: dd \n")
	try:
		date = input("Fecha: ")
		date_list = date.strip().split(":")
		year = str(date_list[0])
		month = str(date_list[1]).zfill(2)
		day = str(date_list[2]).zfill(2)
	except IndexError:
		print("Formato de fecha no valido")
		return True, 0, 0 , 0
	except ValueError:
		print("Formato de fecha invalido")
		return True, 0, 0, 0

	error = False
	if int(year) < 0:
		print("Ano no puede ser negativo")
		error = True
	if int(month) < 0 or int(month) > 12:
		print("Mes ingresado no valido")
		error = True
	if int(day) < 0 or int(day) > 31:
		print("Dia ingresado no valido")
		error = True

	#diccionario con k = cant de dias,  v = meses con esa cantidad
	cant_dias_mes = {30: ["04", "06", "09", "11"], 
	31 : ["01", "03", "05", "07", "08", "10", "12"]}

	if month in cant_dias_mes[30] and int(day) > 30:
		print("Fecha ingresada invalida")
		error = True

	if month in cant_dias_mes[31] and int(day) > 31:
		print("Fecha ingresada invalida")
		error = True

	if month == 2 and is_bisiesto(year) and int(day) > 29:
		print("Fecha ingresada invalida")
		error = True

	if month == 2 and not is_bisiesto(year)	and int(day) > 28:
		print("Fecha ingresada invalida")
		error = True

	return (error, year, month, day)

def set_hora_fecha():

	loop = True
	while loop:
		loop, year, month, day = fecha()
	loop = True
	while loop:
		loop , horas, minutos, segundos = hora()

	fecha_actual = MiFecha((year, month, day), (horas, minutos, segundos))

	return fecha_actual


def set_user():

	loop = True
	while loop:
		loop, user, password = first_menu()

	return user

def menu_ANAF():

	print("*"*20)
	print("Menu Principal".center(10))
	print("Seleccione que operacion desea realizar: ")
	print("\t 1: Desplegar informacion de incendios")
	print("\t 2: Desplegar informacion de recursos")
	print("\t 3: Desplegar informacion de meteorologia")
	print("\t 4: Desplegar informacion de usuarios")
	print("\t 5: Agregar informacion de incendios")
	print("\t 6: Agregar informacion de recursos")
	print("\t 7: Agregar informacion de meteorologia")
	print("\t 8: Agregar informacion de usuario")
	print("\t 9: Realizar consulta")
	print("\t 10: Cambiar fecha y hora")
	print("\t 11: Cerrar sesion")
	print("\t 12: Salir")

	op = int(input("Opcion: "))

	return op

def menu_P_J():

	print("*"*20)
	print("Menu Principal".center(20))
	print("Seleccione la opcion que desea realizar: ")
	print("\t 1: Leer informacion de incendio")
	print("\t 2: Leer informacion de recurso")
	print("\t 3: Cambiar fecha y hora")
	print("\t 4: Cerrar sesion")
	print("\t 5: Salir")

	op = int(input("Opcion: "))

	return op


def desplegar_base_incendios(fecha_actual):

	Incendio.fecha_actual = fecha_actual
	base_incendios = leer_db("incendios.csv", Incendio)
	met_database = leer_db("meteorologia.csv", Meteorologia)

	inc_id = str(input("Ingrese el id del incendio: "))

	try:
		incendio = [inc for inc in base_incendios if inc.id == inc_id].pop()
	except IndexError:
		print("Id no valido")
		return False

	if incendio.fecha_inicio < fecha_actual:
		incendio.simular(met_database, fecha_actual)
		print(incendio)

def desplegar_base_recursos(fecha_actual):

	Recurso.fecha_actual = fecha_actual
	base_recursos = leer_db("recursos.csv", Recurso)

	rec_id = str(input("Ingrese el id del recurso: "))

	recurso = [rec for rec in base_recursos if rec.id == rec_id].pop()

	print(recurso)

def desplegar_base_usuarios():

	base_usuarios = leer_db_usuarios()
	for usuario in base_usuarios:
		print(usuario)

def desplegar_base_meteorologia(fecha_actual):

	Meteorologia.fecha_actual = fecha_actual
	base_meteorologia = leer_db("meteorologia.csv", Meteorologia)
	for met in base_meteorologia:
		print(met)
	

def agregar_usuario():

	nombre = str(input("Ingrese nombre del usuario: "))
	contrasena = str(input("Ingrese contrasena: "))
	recurso_id = str(input("Ingrese el recurso del que esta a cargo: "))

	base_usuarios = leer_db_usuarios()
	id = 0
	for usuario in base_usuarios:
		if int(usuario.id) > int(id):
			id = int(usuario.id)
	id += 1

	with open("usuarios.csv", "r", encoding = "utf8") as af:
		header = af.readline().strip().split(",")
		keys = [f.split(":")[0] for f in header]

		for i in range(len(keys)):
			if keys[i] == "nombre":
				i_nombre = i
			elif keys[i] == "contraseña":
				i_contrasena = i
			elif keys[i] == "recurso_id":
				i_recurso_id = i
			elif keys[i] == "id":
				i_id = i

		orden = []
		orden.append((i_nombre, nombre))
		orden.append((i_recurso_id, recurso_id))
		orden.append((i_contrasena, contrasena))
		orden.append((i_id, id))

		orden.sort()

		msg = ""
		for i, o in orden:
			msg += str(o)
			msg += ","
		msg = msg[:-1]

	with open("usuarios.csv", "a", encoding = "utf8") as af:
		print(msg, file = af)

	print("Usuario agregado exitosamente")
	print("*"*20)


def agregar_meteorologia():

	fecha_i = str(input("Ingrese fecha de inicio en formato aaaa-mm-dd hh:mm:ss : "))
	fecha_t = str(input("Ingrese fecha de termino en formato aaaa-mm-dd hh:mm:ss : "))
	tipo = input("Ingrese el tipo (TEMPERATURA, VIENTO, LLUVIAS o NUBES): ")
	valor = input("Ingrese el valor: ")
	lat = input("Ingrese la latitud: ")
	lon = input("Ingrese la longitud: ")
	radio = input("Ingrese el radio: ")

	base_meteorologia = leer_db("meteorologia.csv", Meteorologia)
	id = 0
	for met in base_meteorologia:
		if int(met.id) > id:
			id = int(met.id)
	id += 1

	with open("meteorologia.csv", "r") as af:
		header = af.readline().strip().split(",")
		keys = [f.split(":")[0] for f in header]

		i_id = keys.index("id")
		i_fecha_inicio = keys.index("fecha_inicio")
		i_fecha_termino = keys.index("fecha_termino")
		i_tipo = keys.index("tipo")
		i_valor = keys.index("valor")
		i_lat = keys.index("lat")
		i_lon = keys.index("lon")
		i_radio = keys.index("radio")

		orden = []
		orden.append((i_id, id))
		orden.append((i_fecha_inicio, fecha_i))
		orden.append((i_fecha_termino, fecha_t))
		orden.append((i_tipo, tipo))
		orden.append((i_valor, valor))
		orden.append((i_lat, lat))
		orden.append((i_lon, lon))
		orden.append((i_radio, radio))

		orden.sort()

		msg = ""
		for i, o in orden:
			msg += str(o)
			msg += ","
		msg = msg[:-1]

	with open("meteorologia.csv", "a") as af:
		print(msg, file = af)

	print("Meteorologia agregado exitosamente")
	print("*"*20)


def agregar_incendio():

	lat = input("Ingrese la latitud: ")
	lon = input("Ingrese la longitud: ")
	pot = input("Ingrese la potencia: ")
	fecha_inicio = input("Ingrese fecha de inicio en formato aaaa-mm-dd hh:mm:ss :")

	base_incendios = leer_db("incendios.csv", Incendio)
	id = 0
	for inc in base_incendios:
		if int(inc.id) > int(id):
			id = int(inc.id)
	id += 1

	with open("incendios.csv", "r") as af:
		header = af.readline().strip().split(",")
		keys = [f.split(":")[0] for f in header]

		i_id = keys.index("id")
		i_fecha_inicio = keys.index("fecha_inicio")
		i_lat = keys.index("lat")
		i_lon = keys.index("lon")
		i_potencia = keys.index("potencia")

		orden = []
		orden.append((i_id, id))
		orden.append((i_fecha_inicio, fecha_inicio))
		orden.append((i_lat, lat))
		orden.append((i_lon, lon))
		orden.append((i_potencia, pot))

		orden.sort()

		msg = ""
		for i, o in orden:
			msg += str(o)
			msg += ","
		msg = msg[:-1]

	with open("incendios.csv", "a") as af:
		print(msg, file = af)

	print("Incendio agregado exitosamente")
	print("*"*20)


def agregar_recurso():

	tipo = input("Ingrese el tipo: ")
	lat = input("Ingrese la latitud: ")
	lon = input("Ingrese la longitud: ")
	vel = input("Ingrese la velocidad: ")
	auto = input("Ingrese la autonomia: ")
	delay = input("Ingrese el delay: ")
	t_ext = input("Ingrese la tasa de extincion: ")
	costo = input("Ingrese el costo: ")

	base_recursos = leer_db("recursos.csv", Recurso)
	id = 0
	for rec in base_recursos:
		if int(rec.id) > id:
			id = int(rec.id)
	id += 1

	with open("recursos.csv", "r") as af:
		header = af.readline().strip().split(",")
		keys = [f.split(":")[0] for f in header]

		i_id = keys.index("id")
		i_tipo = keys.index("tipo")
		i_lat = keys.index("lat")
		i_lon = keys.index("lon")
		i_velocidad = keys.index("velocidad")
		i_autonomia = keys.index("autonomia")
		i_delay = keys.index("delay")
		i_tasa_extincion = keys.index("tasa_extincion")
		i_costo = keys.index("costo")

		orden = []
		orden.append((i_id, id))
		orden.append((i_tipo, tipo))
		orden.append((i_lat, lat))
		orden.append((i_lon, lon))
		orden.append((i_velocidad, vel))
		orden.append((i_autonomia, auto))
		orden.append((i_delay, delay))
		orden.append((i_tasa_extincion, t_ext))
		orden.append((i_costo, costo))

		orden.sort()

		msg = ""
		for i, o in orden:
			msg += str(o)
			msg += ","
		msg = msg[:-1]

	with open("recursos.csv", "a") as af:
		print(msg, file = af)

	print("Recurso agregado exitosamente")
	print("*"*20)


def leer_info_incendio(user):

	if user.asignado:
		id_rec = user.recurso_id
		rec_db = leer_db("recursos.csv", Recurso)
		rec_de_user = [rec for rec in rec_db if rec.id == id_rec].pop()
		print(rec_de_user.incedios_trabajados[-1])

	else:
		print("Usuario no asignado a un incendio")

def leer_info_recurso(user):

	id_rec = user.recurso_id
	rec_db = leer_db("recursos.csv", Recurso)
	rec_to_print = [rec for rec in rec_db if rec.id == id_rec].pop()
	print(rec_to_print)

#esta funcion tarda mucho porque simula para todos los incendios e imprime los activos
def desplegar_incendios_activos(fecha_actual):
	
	met_database = leer_db("meteorologia.csv", Meteorologia)
	inc_db = leer_db("incendios.csv", Incendio)
	for inc in inc_db:
		if inc.fecha_inicio < fecha_actual:
			inc.simular(met_database, fecha_actual)
			if inc.activo:
				print(inc)

def desplegar_incendios_apagados(fecha_actual):

	inc_db = leer_db("incendios.csv", Incendio)
	for inc in inc_db:
		if inc.fecha_inicio < fecha_actual:
			inc.simular(fecha_actual)
			if not inc.activo:
				msg = str(inc)
				msg += "|Fecha de cese: ".format(inc.fecha_cese) + "|"
				msg += "|Recursos utilizados: ".format([repr(rec) for rec in inc.recursos_utilizados])

				print(msg)

def desplegar_rec_utilizados(*args):
	print("No implementado")

def desplegar_rec_efectivos(*args):
	print("No implementado")


if __name__ == "__main__":
	print("*"*20)
	print("Bienvenido a SuperLuchin")

	user = set_user()
	#fecha_actual = set_hora_fecha()
	fecha_actual = MiFecha((2017,3,23), (20, 4, 0))

	dict_options_ANAF = {1: desplegar_base_incendios, 2: desplegar_base_recursos,
	3: desplegar_base_meteorologia, 4: desplegar_base_usuarios,
	5: agregar_incendio, 6: agregar_recurso, 7:agregar_meteorologia,
	8: agregar_usuario}

	loop = True
	while loop:
		if isinstance(user, UsuarioANAF):
			try:
				op = int(menu_ANAF())
			except ValueError:
				print("Opcion invalida")

			if op in dict_options_ANAF:
				if op == 1:
					desplegar_base_incendios(fecha_actual)
				elif op == 2:
					desplegar_base_recursos(fecha_actual)
				elif op == 3:
					desplegar_base_meteorologia(fecha_actual)
				else:
					dict_options_ANAF[op]()


			elif op == 9:
				dict_options_avanzada = {1: desplegar_incendios_activos,
				2: desplegar_incendios_apagados, 3: desplegar_rec_utilizados,
				4: desplegar_rec_efectivos}
				print("*"*20)
				print("Indique que consulta desea realizar:")
				print("\t 1: Desplegar incendios activos")
				print("\t 2: Desplegar incendios apagados")
				print("\t 3: Desplegar recusos mas utilizados")
				print("\t 4: Desplegar recursos mas efectivos")
				op_consulta_av = int(input("Opcion: "))

				if op_consulta_av in dict_options_avanzada:
					dict_options_avanzada[op_consulta_av](fecha_actual)
				else:
					print("Opcion invalida")
			elif op ==10:
				fecha_actual = set_hora_fecha()
			elif op == 11:
				user = set_user()
			elif op == 12:
				print("Gracias por usar SuperLuchin")
				loop = False
			else:
				print("Opcion invalida")

		else:
			leer_info_recurso(user)
			try:
				op = int(menu_P_J())
			except ValueError:
				print("Opcion invalida")

			if op == 1:
				leer_info_incendio(user)
			elif op == 2:
				leer_info_recurso(user)
			elif op == 3:
				fecha_actual = set_hora_fecha()
			elif op ==4:
				user = set_user()
			elif op == 5:
				print("Gracias por usar SuperLuchin")
				loop = False
			else:
				print("Opcion invalida")







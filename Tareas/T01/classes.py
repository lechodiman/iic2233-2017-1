from math import sqrt, pi
from functions import intersect, is_bisiesto, grados_a_puntos, dist_entre_grados

def leer_db(nombre_archivo, clase):
	with open(nombre_archivo, "r") as rf:
		header = rf.readline().strip().split(",")
		keys = [f.split(":")[0] for f in header]
		lista_objetos = []
		for line in rf:
			dict_objeto = dict()
			for i in range(len(keys)):
				dict_objeto[keys[i]] = line.strip().split(",")[i]

			lista_objetos.append(clase.from_dict(dict_objeto))
		
		return lista_objetos


def leer_db_usuarios():
	with open("usuarios.csv", "r", encoding = "utf8") as rf:
		header = rf.readline().strip().split(",")
		keys = [f.split(":")[0] for f in header]
		lista_usuarios = []
		for line in rf:
			dict_user = dict()
			linea_separados = line.strip().split(",")
			for i in range(min(len(linea_separados), len(keys))):
				dict_user[keys[i]] = linea_separados[i]

			if not "recurso_id" in dict_user:
				dict_user["recurso_id"] = ""

			recurso_user_id = dict_user["recurso_id"]
			recursos_db = leer_db("recursos.csv", Recurso)

			tipo_recurso = ""
			for recurso in recursos_db:
				if recurso_user_id == recurso.id:
					tipo_recurso = recurso.tipo

			if tipo_recurso == 'BOMBEROS' or tipo_recurso == 'BRIGADA':
				clase_user = Jefe
			elif tipo_recurso == 'HELICOPTERO' or tipo_recurso == 'AVION':
				clase_user = Piloto
			else:
				clase_user = UsuarioANAF

			lista_usuarios.append(clase_user.from_dict(dict_user))

		return lista_usuarios


class MiFecha:

	def __init__(self, fecha = tuple(), hora = tuple()):
		self.ano, self.mes, self.dia = [int(i) for i in fecha]
		self.horas, self.minutos, self.segundos = [int(i) for i in hora]

	@property
	def dict_cant_dias(self):
		d = {1: 31 , 2: 29 if is_bisiesto(self.ano) else 28,
		3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

		return d

	def __lt__(self, other):

		if self.ano != other.ano:
			return self.ano < other.ano
		elif self.mes != other.mes:
			return self.mes < other.mes
		elif self.dia != other.dia:
			return self.dia < other.dia
		elif self.horas != other.horas:
			return self.horas < other.horas
		elif self.minutos != other.minutos:
			return self.minutos < other.minutos
		elif self.segundos != other.segundos:
			return self.segundos < other.segundos
		else:
			return False

	def __eq__(self, other):
		bool1 = self.ano == other.ano and self.mes == other.mes and self.dia == other.dia
		bool2 = self.horas == other.horas and self.minutos == other.minutos and self.segundos == other.segundos

		return (bool1 and bool2)

	def __sub__(self, other):
		dif = 0
		dif += (self.ano - other.ano) * 525600
		dif += (self.mes - other.mes) * 43800
		dif += (self.dia - other.dia) * 1440
		dif += (self.horas - other.horas) * 60
		dif += (self.minutos - other.minutos)
		dif += (self.minutos - other.minutos) * (1/60)

		return dif #retorna la diferencia de tiempo en minutos entre dos fechas


	#Asumo que no le sumare una cantidad de segundos superior a un mes
	def sumar_segundos(self, t_segundos):
		self.segundos += t_segundos

		if self.segundos > 60:
			min_extra = self.segundos // 60
			self.segundos %= 60
			self.minutos += min_extra

		if self.minutos > 60:
			horas_extra = self.minutos // 60
			self.minutos %= 60
			self.horas += horas_extra

		if self.horas > 24:
			dias_extra = self.horas // 24
			self.horas %= 24
			self.dia += dias_extra

		if self.dia > self.dict_cant_dias[int(self.mes)]:
			mes_extra = self.dia // self.dict_cant_dias[int(self.mes)]
			self.dia %= self.dict_cant_dias[self.mes]
			self.mes += mes_extra

		if self.mes > 12:
			ano_extra = self.mes // 12
			self.mes %= 12
			self.ano += ano_extra

	def copy(self):
		return MiFecha((self.ano, self.mes, self.dia), (self.horas, self.minutos, self.segundos))


	def __str__(self):
		msg = str(self.ano) + "-"
		msg += str(self.mes) + "-"
		msg += str(self.dia) + "-"  + " "
		msg += str(self.horas).zfill(2) + ":"
		msg += str(self.minutos).zfill(2) + ":"
		msg += str(self.segundos).zfill(2)

		return msg

	@classmethod
	def from_str(cls, string):
		fecha_hora = string.split(" ")
		year, month, day = fecha_hora[0].split("-")
		horas, minutos, segundos = fecha_hora[1].split(":")

		return cls((year, month, day),(horas, minutos, segundos))



class Incendio:
	fecha_actual = ""

	def __init__(self, id, lat, lon, pot, fecha_inicio):
		self.id = id
		self.ubicacion = (lat, lon)
		self.potencia = pot
		self.fecha_inicio = MiFecha.from_str(fecha_inicio)
		self.radio = 1
		self.puntos_poder_extintos = 0
		self.recursos_utilizados = []
		self.fecha_cese = None
		self.recursos_trabajando = []
		self.lat = lat
		self.lon = lon

	@classmethod
	def from_dict(cls, dict_incendio):
		id = str(dict_incendio["id"])
		lat, lon = float(dict_incendio["lat"]), float(dict_incendio["lon"])
		potencia = int(dict_incendio["potencia"])
		fecha_inicio = str(dict_incendio["fecha_inicio"])

		return cls(id, lat, lon, potencia, fecha_inicio)

	def recibir_recurso(self, recurso):
		self.recursos_utilizados.append(recurso)
		fechas = recurso.fechas_salidas[-1]
		#t_trabajo = fecha retirada - fecha llegada
		t_trabajo = fechas[2] - fechas[1]

		for minute in range(int(t_trabajo)):
			self.puntos_poder -= recurso.tasa_ext / 60
			self.puntos_poder_extintos += recurso.tasa_ext / 60

	@property
	def porcentaje_ext(self):
		return float(self.puntos_poder_extintos / self.puntos_poder)

	@property
	def activo(self):
		return self.puntos_poder > 0

	@property
	def puntos_poder(self):
		return self.potencia * self.superficie_afectada

	@property
	def superficie_afectada(self):
		return pi * self.radio**2

	def hay_nubes(self, altura, fecha = fecha_actual):
		met_database = leer_db("meteorologia.csv", Meteorologia)

		#lista con reportes meteorologicos de nubes que afectan a la fecha
		met_nubes = [met for met in met_database if met.tipo == 'NUBES' and \
					fecha < met.fecha_termino and fecha > met.fecha_inicio]

		x_inc, y_inc = grados_a_puntos(self.lat, self.lon)
		r_inc = self.radio

		met_nubes_en_radio = []

		for met in met_nubes:
			x_met, y_met = grados_a_puntos(met.lat, met.lon)
			r_met = met.radio
			cond_intersect = intersect(x_inc, y_inc, r_inc, x_met, y_met, r_met)
			if cond_intersect:
				met_nubes_en_radio.append(met)

		ultimo_reporte = max(met_nubes_en_radio)

		if ultimo_reporte.valor >= altura:
			return True
		else:
			return False


	def simular(self, met_database, fecha = fecha_actual):
		if fecha < self.fecha_inicio:
			return False

		delta_tiempo = fecha - self.fecha_inicio #retorna diferencia en minutos entre fechas
		met_entre_fechas = []

		for met in met_database:
			if met.fecha_inicio < fecha and met.fecha_termino > fecha:
				met_entre_fechas.append(met)

		t_en_simulacion = self.fecha_inicio.copy()

		for minute in range(int(delta_tiempo)):
			self.radio += 8.333
			for met in met_entre_fechas:
				x_inc, y_inc = grados_a_puntos(self.lat, self.lon)
				r_inc = self.radio
				x_met, y_met = grados_a_puntos(met.lat, met.lon)
				r_met = met.radio

				cond_1 = met.fecha_inicio < t_en_simulacion and met.fecha_termino > t_en_simulacion
				cond_2 = intersect(x_inc, y_inc, r_inc, x_met, y_met, r_met)

				if cond_1 and cond_2:
					if met.tipo == 'VIENTO':
						self.radio += 60 * (met.valor / 100)
					elif met.tipo == 'TEMPERATURA':
						if met.valor > 30:
							self.radio += 25 * (int(met.valor) - 30) / 60
					elif met.tipo == 'LLUVIA':
						self.radio -= 50 * met.valor / 60



				#En el caso de que el incendio se apague por lluvias
				if self.radio <= 0:
					self.fecha_cese = t_en_simulacion.copy()
					break

			t_en_simulacion.sumar_segundos(60)


	def __str__(self):
		estado = "Apagado"
		if self.activo:
			estado = "Activo"

		rec = (str(i) for i in self.recursos_trabajando)
		rec_str = "("
		for i in rec:
			rec_str += i
		rec_str += ")"

		msg = "|"
		msg += "ID: " + str(self.id) + "|"
		msg += "Ubicacion: {}".format(self.ubicacion) +"|"
		msg += "Potencia: {}".format(self.potencia) + "|"
		msg += "Puntos de poder {}".format(self.puntos_poder) + "|"
		msg += "Fecha inicio: {}".format(self.fecha_inicio) + "|"
		msg += "Estado actual: " + str(estado) + "|"
		msg += "Porcentaje extincion: " + str(self.porcentaje_ext)  +"|"
		msg += "Recursos trabajando: " + rec_str + "|"
		
		return msg



class Recurso:

	fecha_actual = ""

	def __init__(self, id, tipo, velocidad, lat, lon, auto,
				 delay, tasa_ext, costo):
		self.id = id
		self.tipo = tipo
		self.velocidad = velocidad
		self.ubicacion_base = (lat, lon)
		self.autonomia = auto
		self.delay = delay
		self.tasa_ext = tasa_ext
		self.costo = costo
		self.tiempo_trabajado = 0
		self.dist_a_objetivo = 0
		self.incendios_trabajados = []
		if self.tipo == "HELICOPTERO":
			self.techo = 1000
		elif self.tipo == 'AVION':
			self.techo = 1500
		else:
			self.techo = 1000000
		self.fechas_salidas = [] #contiene tuplas con (salida, llegada, retirada, regreso )


	@classmethod
	def from_dict(cls, dict_recurso):
		id = str(dict_recurso["id"])
		tipo = str(dict_recurso["tipo"])
		lat, lon = float(dict_recurso["lat"]), float(dict_recurso["lon"])
		velocidad = int(dict_recurso["velocidad"])
		autonomia = int(dict_recurso["autonomia"])
		delay = int(dict_recurso["delay"])
		tasa_extincion = int(dict_recurso["tasa_extincion"])
		costo = int(dict_recurso["costo"])

		return cls(id, tipo, velocidad, lat, lon, autonomia, delay, tasa_extincion,
			costo)

	@property
	def estado_actual(self, fecha = fecha_actual):
		for incursion in self.fechas_salidas:
			#si esta entre la salida y la llegada
			if fecha < incursion[1] and fecha > incursion[0]:
				return "en ruta a incendio"
			#si esta entre el regreso y la retirada			
			elif fecha < incursion[3] and fecha > incursion[2]:
				return "en ruta a base"
			#si esta entre la retirada y la llegada
			elif fecha < incursion[2] and fecha > incursion[1]:
				return "trabajando en incendio"

		return "standby"


	@property
	def ubicacion_actual(self):
		if self.estado_actual == "standby":
			return self.ubicacion_base
		elif self.estado_actual == "en ruta a incendio":
			pass
		elif self.estado_actual == "trabajando en incendio":
			return self.incendios_trabajados[-1].ubicacion
		elif self.estado_actual == "en ruta a base":
			pass

	def enviar_a_incendio(self, incendio, fecha = fecha_actual):
		if (self.tipo == 'HELICOPTERO' or self.tipo == 'AVION') and incendio.hay_nubes(self.techo):
			return False

		self.incendios_trabajados.append(incendio)

		d_viaje = dist_entre_grados(incendio.ubicacion, self.ubicacion_base) #dist en km
		t_viaje = d_viaje * 1000 / self.velocidad #tiempo en segundos
		print("Hora de salida: {}".format(str(fecha)))
		hora_llegada = fecha.copy().sumar_segundos(t_viaje)
		print("Hora de llegada: {}".format(str(hora_llegada)))
		hora_retirada = hora_llegada.copy().sumar_segundos(self.autonomia * 3600)
		print("Hora de retirada: {}".format(str(hora_retirada)))
		hora_regreso = hora_retirada.copy().sumar_segundos(t_viaje)
		print("Hora de regreso: {}".format(str(hora_regreso)))

		self.fechas_salidas.append((fecha, hora_llegada, hora_retirada, hora_regreso))

	def __str__(self):
		msg = ""
		msg += "|Id: {}".format(self.id) + "|"
		msg += "|Tipo: {}".format(self.tipo) + "|"
		msg += "|Velocidad: {}".format(self.velocidad) + "|"
		msg += "|Ubicacion base: {}".format(self.ubicacion_base) + "|"
		msg += "|Autonomia: {}".format(self.autonomia) + "|"
		msg += "|Delay: {}".format(self.delay) + "|"
		msg += "|Tasa ext: {}".format(self.tasa_ext) + "|"
		msg += "|Costo: {}".format(self.costo) + "|"
		msg += "|Ubicacion actual: {}".format(self.ubicacion_actual) + "|"
		msg += "|Estado actual: {}".format(self.estado_actual) + "|"

		if self.estado_actual == "trabajando en incendio":
			msg += "|Tiempo trabajado: " + "|"
			msg += "|Tiempo restante: " +  "|"


		elif self.estado_actual == "en ruta a base":
			dist_a_obj = dist_entre_grados(self.ubicacion_actual, self.incendios_trabajados[-1].ubicacion)
			msg += "|Distancia hacia objetivo: ".format(dist_a_obj)

		return msg

	def __repr__(self):
		msg = "Recurso({},{})".format(self.id, self.tipo)

		return msg


class Meteorologia:

	def __init__(self, id, fecha_i, fecha_t, tipo, valor,
				lat, lon, radio):
		self.id = id
		self.fecha_inicio = MiFecha.from_str(fecha_i)
		self.fecha_termino = MiFecha.from_str(fecha_t)
		self.tipo = tipo
		self.valor = valor
		self.ubicacion = (lat, lon)
		self.radio = radio
		self.lat = lat
		self.lon = lon

	@classmethod
	def from_dict(cls, dict_met):
		id = str(dict_met["id"])
		fecha_inicio = str(dict_met["fecha_inicio"])
		fecha_termino = str(dict_met["fecha_termino"])
		tipo = str(dict_met["tipo"])
		valor = float(dict_met["valor"])
		lat, lon = float(dict_met["lat"]), float(dict_met["lon"])
		radio = int(dict_met["radio"])

		return cls(id, fecha_inicio, fecha_termino, tipo, valor, lat, lon, radio)

	def __str__(self):
		msg = "|"
		msg += "ID: {}".format(self.id) + "|"
		msg += "Fecha inicio: {}".format(self.fecha_inicio) + "|"
		msg += "Fecha termino: {}".format(self.fecha_termino) + "|"
		msg += "Tipo : {}".format(self.tipo) + "|"
		msg += "Valor: {}".format(self.valor) + "|"
		msg += "Ubicacion {}".format(self.ubicacion) + "|"
		msg += "Radio {}".format(self.radio) + "|"

		return msg

	def __lt__(self, other):
		return self.fecha_inicio < other.fecha_inicio


class Usuario:

	def __init__(self, id, nombre, contrasena, recurso_id = None):
		self.id = id
		self.nombre = nombre
		self.contrasena = contrasena
		if recurso_id != None:
			self.recurso_id = recurso_id
	
	@classmethod
	def from_dict(cls, dict_user):
		id = str(dict_user["id"])
		nombre = str(dict_user["nombre"])
		contrasena = str(dict_user["contraseña"])
		recurso_id = str(dict_user["recurso_id"])

		return cls(id, nombre, contrasena, recurso_id)

	def __str__(self):
		msg = "|"
		msg += "Nombre: {}".format(self.nombre) +"|"
		msg += "Id de recurso: {}".format(self.recurso_id) + "|"

		return msg


class UsuarioANAF(Usuario):
	def __init__(self, id, nombre, contrasena, recurso_id = None):
		super().__init__(id, nombre, contrasena, recurso_id)

class Piloto(Usuario):
	def __init__(self, id , nombre, contrasena, recurso_id):
		super().__init__(id, nombre, contrasena, recurso_id)
		self.asignado = False

class Jefe(Usuario):
	def __init__(self, id , nombre, contrasena, recurso_id):
		super().__init__(id, nombre, contrasena, recurso_id)
		self.asignado = False
	






	 		
















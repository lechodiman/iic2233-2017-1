__author__ = 'lechodiman'

import random
from bernoulli_event import bernoulli
from collections import deque


class Replica:

    def __init__(self):
        x = bernoulli(0.7)
        if x == 1:
            tipo = 'debil'
        else:
            tipo = 'fuerte'

        if tipo == 'debil':
            self.prob_no_sobrevivir_caminando = 0.1
            self.prob_no_sobrevivir_vehiculo = 0.15
            self.prob_tsunami = 0
            self.potencia_tsunami = 0
        else:
            self.prob_no_sobrevivir_caminando = 0.3
            self.prob_no_sobrevivir_vehiculo = 0.6
            self.prob_tsunami = 0.7
            self.potencia_tsunami = random.randint(3, 8)


class Tsunami:

    def __init__(self, potencia):
        self.centro = random.uniform(0, 100)
        self.potencia = potencia
        self.alcance = potencia * 4
        self.prob_no_sobrevivir = self.potencia / 10

    @property
    def range_in_rute(self):
        return (self.centro - self.potencia / 2, self.centro + self.potencia / 2)


class Persona:

    def __init__(self):
        self.personalidad = random.choice(['generoso', 'egoista'])
        if self.personalidad == 'generoso':
            self.prob_detenerse = 0.6
        else:
            self.prob_detenerse = 0.3
        self.rapidez_pie = random.uniform(5, 8)
        self.posicion_inicial = random.randint(0, 60)
        self.posicion = self.posicion_inicial
        self.vehiculo = None
        self.alive = True
        self.is_conductor = False
        self.death_reason = None

    @property
    def in_vehicle(self):
        has_v = self.vehiculo is not None
        return has_v

    @property
    def rapidez(self):
        if self.in_vehicle:
            return self.vehiculo.rapidez
        else:
            return self.rapidez_pie

    @property
    def is_safe(self):
        return self.posicion >= 100

    def kill(self, reason):
        if self.alive:
            self.alive = False
            self.death_reason = reason

    def actualizar_posicion(self, tiempo):
        if self.alive:
            self.posicion = self.posicion_inicial + self.rapidez * tiempo

    def dar_vehiculo(self, vehiculo):
        if self.vehiculo is not None:
            self.vehiculo = vehiculo
            vehiculo.agregar_pasajero(self)

    def kill_vehicle(self, reason):
        if self.in_vehicle and self.alive:
            for p in self.vehiculo.pasajeros:
                p.kill(reason)


class Vehiculo:

    def __init__(self):
        x = bernoulli(0.5)
        if x == 1:
            self.tipo = 'auto'
        else:
            self.tipo = 'camioneta'

        self.rapidez = random.uniform(12, 20)
        if self.tipo == 'auto':
            self.capacidad = 5
        else:
            self.capacidad = 8
        self.pasajeros = []

    def agregar_pasajero(self, pasajero):
        if len(self.pasajeros) < self.capacidad:
            if len(self.pasajeros) == 0:
                pasajero.is_conductor = True
            pasajero.vehiculo = self
            self.pasajeros.append(pasajero)

    def get_conductor(self):
        return self.pasajeros[0]


class Simulacion:

    def __init__(self, n_personas=100, tiempo_maximo=200):
        self.n_personas = n_personas
        self.poblacion = [Persona() for i in range(n_personas)]
        self.vehiculos = []
        for i in range(25):
            p = random.choice(self.poblacion)
            v = Vehiculo()
            self.vehiculos.append(v)
            p.dar_vehiculo(v)
        self.lista_evento = list()
        self.tiempo_maximo = tiempo_maximo
        self.tiempo_total_simulacion = 0

    def ordenar_lista(self):
        self.lista_eventos.sort(key=lambda x: x[0])

    def tiempo_llegada_replica(self, tiempo):
        self.lista_eventos.append((tiempo + random.expovariate(1 / random.randint(4, 10)), 'llegada replica'))

    def llegada_replicas(self, tiempo):
        print("[{}] llego una replica".format(tiempo))
        self.tiempo_llegada_replica(tiempo)
        r = Replica()
        # matar y generar tsunami
        for i in self.poblacion:
            if not i.is_safe:
                if i.in_vehicle:
                    # 1 if he dies, 0 eoc
                    x = bernoulli(r.prob_no_sobrevivir_vehiculo)
                    if x == 1:
                        i.kill_vehicle(reason='replica')
                else:
                    x = bernoulli(r.prob_no_sobrevivir_caminando)
                    if x == 1:
                        i.kill(reason='replica')
        # let g = 1 if r generates a marepoto, 0 eoc
        g = bernoulli(r.prob_tsunami)
        if g == 1:
            self.llegada_tsunami(tiempo, r.potencia_tsunami)

    def llegada_tsunami(self, tiempo, potencia_tsunami):
        print("[{}] llego un tsunami".format(tiempo))
        t = Tsunami(potencia_tsunami)
        rango_inf = t.range_in_rute[0]
        rango_sup = t.range_in_rute[1]
        for i in self.poblacion:
            if not i.is_safe:
                if i.in_vehicle:
                    if i.posicion <= rango_sup and i.posicion >= rango_inf:
                        x = bernoulli(t.prob_no_sobrevivir)
                        if x == 1:
                            i.kill_vehicle(reason='tsunami')
                else:
                    if i.posicion <= rango_sup and i.posicion >= rango_inf:
                        x = bernoulli(t.prob_no_sobrevivir)
                        if x == 1:
                            i.kill(reason='tsunami')

    def update_positions(self, tiempo):
        for i in self.poblacion:
            i.actualizar_posicion(tiempo)

    def run(self):
        tiempo = 0
        self.tiempo_llegada_replica(tiempo)

        while len(self.lista_eventos) != 0:
            tiempo, evento = self.lista_eventos[0]

            self.tiempo_total_simulacion = tiempo

            self.lista_eventos = self.lista_eventos[1:]
            if tiempo > self.tiempo_maximo:
                tiempo = self.tiempo_maximo
                self.tiempo_total_simulacion = tiempo
                break

            alive = [p for p in self.poblacion if p.alive]
            safe = [p for p in self.poblacion if p.is_safe]
            if len(alive) == 0 or len(safe) == self.n_personas:
                print("[{}] no quedan personas en Calle Larga".format(tiempo))
                break

            self.update_positions(tiempo)

            # aca deberia subir gente a los autos de acuerdo a alguna func

            if evento == 'llegada replica':
                self.llegada_replicas(tiempo)

            self.ordenar_lista()


def get_statistics(n_reps=10):
    n_car = 0
    n_camioneta = 0
    n_generoso = 0
    n_egoista = 0
    t_total = 0
    n_dead_replica = 0
    n_dead_tsunami = 0

    for i in range(n_reps):
        s = Simulacion()
        s.run()

        dead_people = [p for p in s.poblacion if not p.alive]
        dead_with_replica = sum([d for d in dead_people if d.death_reason == 'replica'])
        dead_with_tsunami = sum([d for d in dead_people if d.death_reason == 'tsunami'])

        n_dead_replica += dead_with_replica
        n_dead_tsunami += dead_with_tsunami

        for v in s.vehiculos:
            if v.tipo == 'auto':
                if v.get_conductor().is_safe:
                    n_car += 1
            elif v.tipo == 'camioneta':
                if v.get_conductor().is_safe:
                    n_camioneta += 1

        for p in s.poblacion:
            if p.personalidad == 'generoso' and p.is_safe:
                n_generoso += 1
            elif p.personalidad == 'egoista' and p.is_safe:
                n_egoista += 1
        t_total += s.tiempo_total_simulacion

    avg_car = n_car / n_reps
    avg_camioneta = n_camioneta / n_reps
    avg_generoso = n_generoso / n_reps
    avg_egoista = n_egoista / n_reps
    avg_t_total = t_total / n_reps
    avg_dead_replica = n_dead_replica / n_reps
    avg_dead_tsunami = n_dead_tsunami / n_reps

    print(avg_car)
    print(avg_camioneta)
    print(avg_generoso)
    print(avg_egoista)
    print(avg_t_total)
    print(avg_dead_replica)
    print(avg_dead_tsunami)

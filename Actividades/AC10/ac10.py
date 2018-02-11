import threading
import random
import time


class Pieza:
    def __init__(self, value):
        self.value = value
        self.piezas_adyancentes = []

    def add_conexion(self, pieza):
        self.piezas_adyancentes.append(pieza)

    def __repr__(self):
        return self.value


class Laberinto:
    def __init__(self, file):
        self.piezas = []
        self.personas = []
        self.personas_muertas = []
        self.values = []
        self.pieza_inicio = None
        self.pieza_final = None
        self.file = file
        self.personas_finalistas = []

    def get_pieza_inicio(self):
        pieza = [room for room in self.piezas if room.value == self.pieza_inicio].pop()
        return pieza

    def get_pieza_final(self):
        pieza = [room for room in self.piezas if room.value == self.pieza_final].pop()
        return pieza

    def unir_piezas(self, v_1, v_2):
        if v_1 not in self.values:
            p_1 = Pieza(v_1)
            self.values.append(v_1)
            self.piezas.append(p_1)
        else:
            p_1 = [p for p in self.piezas if p.value == v_1].pop()

        if v_2 not in self.values:
            p_2 = Pieza(v_2)
            self.values.append(v_2)
            self.piezas.append(p_2)
        else:
            p_2 = [p for p in self.piezas if p.value == v_2].pop()

        p_1.add_conexion(p_2)

    def load(self):
        with open(self.file, 'r', encoding='utf-8') as ar:
            lines_ar = (line.rstrip('\n').strip() for line in ar)
            first = next(lines_ar)
            last = next(lines_ar)
            self.pieza_inicio = first
            self.pieza_final = last
            for line in lines_ar:
                new_line = line.split(',')
                v_1 = new_line[0]
                v_2 = new_line[1]

                self.unir_piezas(v_1, v_2)

    def agregar_persona(self, p):
        if p not in self.personas:
            p.pieza_actual = self.get_pieza_inicio()
            self.personas.append(p)
            print('Se agrego a la persona {}'.format(p.ID))

    def get_statistics(self):
        with open('estadisticas_laberinto.txt', 'w') as rf:
            for person in self.personas_finalistas:
                output = "Persona{} - {} - {}".format(person.ID, person.final_simulation_time, person.final_time)
                rf.write(output + '\n')
            n_dead = len(self.personas_muertas)
            rf.write('Muertos: {}'.format(n_dead) + '\n')
            try:
                average_survival_time = sum([person.death_time for person in self.personas_muertas]) / len(self.personas_muertas)
            except ZeroDivisionError:
                average_survival_time = 0
            rf.write('Promedio tiempos supervivencia: {}'.format(average_survival_time) + '\n')


class Persona(threading.Thread):
    lock_pieza = threading.Lock()

    def __init__(self):
        super().__init__()
        self.ID = next(Persona.get_i)
        self.hp = random.randrange(80, 121)
        self.pieza_actual = None
        self.resistance = random.randrange(1, 4)
        self.start_time = time.time()
        self.final_time = None
        self.death_time = None
        self.final_simulation_time = None

    @property
    def vivo(self):
        if self.hp <= 0:
            return False
        else:
            return True

    def atacado_toxina(self):
        self.hp -= 6 - self.resistance
        print("La persona {} ha sido danada!!  HP {} ".format(self.ID, self.hp))
        if not self.vivo:
            self.death_time = time.time() - self.start_time
            print("La persona {} ha muerto !!!".format(self.ID))

    def run(self):
        while self.vivo and len(l.personas_finalistas) < 3:
            if self.pieza_actual != l.get_pieza_inicio() and self.pieza_actual != l.get_pieza_final():
                Persona.lock_pieza.acquire()
                time.sleep(random.randrange(1, 4))
                Persona.lock_pieza.release()
                self.pieza_actual = random.choice(self.pieza_actual.piezas_adyancentes)
                print('La persona {} se movio a la pieza {}'.format(self.ID, self.pieza_actual))
                if self.pieza_actual == l.get_pieza_final():
                    l.personas_finalistas.append(self)
                    self.final_time = time.time() - self.start_time
                    self.final_simulation_time = time.clock()
                    print('La persona {} llego al final'.format(self.ID))

            elif self.pieza_actual == l.get_pieza_inicio():
                time.sleep(random.randrange(1, 4))
                self.pieza_actual = random.choice(self.pieza_actual.piezas_adyancentes)
                print('La persona {} se movio a la pieza {}'.format(self.ID, self.pieza_actual))
                if self.pieza_actual == l.get_pieza_final():
                    l.personas_finalistas.append(self)
                    self.final_time = time.time() - self.start_time
                    self.final_simulation_time = time.clock()
                    print('La persona {} llego al final'.format(self.ID))

    def __repr__(self):
        return str(self.ID)

    def id_():
        i = 0
        while True:
            yield i
            i += 1

    get_i = id_()


def spawner(laberinto):
    while len(laberinto.personas_finalistas) < 3:
        time.sleep(random.expovariate(1 / 5))
        p = Persona()
        p.setDaemon(True)
        laberinto.agregar_persona(p)
        p.start()

    print('FIN de la simulacion')


def limpiador(laberinto):
    while True:
        time.sleep(0.01)
        for person in laberinto.personas:
            if not person.vivo:
                print('[LIMPIADOR] retiro a la persona {}'.format(person))
                laberinto.personas_muertas.append(person)
                laberinto.personas.remove(person)


def toxina(laberinto):
    while True:
        time.sleep(1)
        for person in laberinto.personas:
            person.atacado_toxina()


l = Laberinto('laberinto.txt')
l.load()
s = threading.Thread(target=spawner, args=(l, ))
t = threading.Thread(target=toxina, args=(l, ), daemon=True)
claner = threading.Thread(target=limpiador, args=(l, ), daemon=True)

time.clock()
s.start()
t.start()
claner.start()

s.join()
l.get_statistics()

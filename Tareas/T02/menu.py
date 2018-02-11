from linked_lists import LinkedList, LinkedQueue
from connections_generator import generate_connections
from abc import ABCMeta
from bernoulli_event import bernoulli, uniform
from proposal import Proposal
from random import choice
import csv
from matplotlib import pyplot as plt
import numpy as np


class Infection(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name


class Virus(Infection):
    def __init__(self, name):
        super().__init__(name)
        self.tasa_contagiosidad = 1.5
        self.tasa_mortalidad = 1.2
        self.resistencia_medicina = 1.5
        self.visibilidad = 0.5


class Bacteria(Infection):
    def __init__(self, name):
        super().__init__(name)
        self.tasa_contagiosidad = 1
        self.tasa_mortalidad = 1
        self.resistencia_medicina = 0.5
        self.visibilidad = 0.7


class Parasite(Infection):
    def __init__(self, name):
        super().__init__(name)
        self.tasa_contagiosidad = 0.5
        self.tasa_mortalidad = 1.5
        self.resistencia_medicina = 1
        self.visibilidad = 0.45


class Game:
    def __init__(self, world):
        self.world = world

    def choose_infection(self):
        loop = True
        while loop:
            print("Escoja el tipo de infeccion que desea utilizar: ")
            print("\t[1] Virus ")
            print("\t[2] Bacteria ")
            print("\t[3] Parasito ")

            try:
                user_infection = int(input("Eleccion: "))
                if user_infection > 3 or user_infection < 0:
                    raise ValueError
            except ValueError:
                print("Opcion ingresada no valida")
                print("-" * 50)
            else:
                loop = False
        infection_name = input("Nombre de la infeccion: ")

        if user_infection == 1:
            infection = Virus(infection_name)
        elif user_infection == 2:
            infection = Bacteria(infection_name)
        elif user_infection == 3:
            infection = Parasite(infection_name)

        self.world.infection = infection

    def choose_country(self):
        loop = True
        while loop:
            print("Escoja el pais donde empezara la enfermedad: ")
            for country in self.world.countries:
                print("Nombre: ", str(country.name), "\t", "|", str(country.initial_population))
            print("*" * 20)
            try:
                user_country = input("Seleccion: ").title()
                if user_country not in self.world.names:
                    raise ValueError
            except ValueError as err:
                print("[ERROR] El pais no es valido")
                loop = True
            else:
                loop = False

        print("{} se ha desatado en el pais: {}".format(self.world.infection.name.title(), user_country))
        country = self.world.countries.find_name(user_country)
        country.infect_one()

    def main_menu(self):
        print("Menu Principal")
        print("-" * 20)
        print("Dia ACTUAL \t: {}".format(self.world.day))
        msg_infection_detected = "Si" if world.infection_detected else "No"
        print("Infeccion descubierta \t: {}".format(msg_infection_detected))
        print("Progreso de la cura \t: {}".format(world.cure_progress))
        print("-" * 20)
        loop = True
        while loop:
            print("Seleccione una opcion: ")
            print("\t [1] Pasar de dia")
            print("\t [2] Mostrar estadisticas")
            print("\t [3] Guardar juego")
            print("\t [4] Salir")

            try:
                option_input = int(input("Eleccion: ").strip())
                if option_input > 4 or option_input < 0:
                    raise ValueError
            except ValueError:
                print("Opcion ingresada no valida")
                print("-" * 20)
            else:
                loop = False
        return option_input

    def statistics_menu(self):
        print("Menu Estadisticas")
        print("-" * 20)
        print("Dia ACTUAL \t: {}".format(self.world.day))
        print("-" * 20)
        loop = True
        while loop:
            print("Seleccione una opcion: ")
            print("\t [1] Sitacion del pais")
            print("\t [2] Situacion del mundo")
            print("\t [3] Promedios de infeccion y muerte")
            print("\t [4] Resumen sucesos del dia")
            print("\t [5] Tabla de muertos e infectados por dia")
            print("\t [6] Volver")

            try:
                option_input = int(input("Eleccion: ").strip())
                if option_input > 6 or option_input < 0:
                    raise ValueError
            except ValueError:
                print("Opcion ingresada no valida")
                print("-" * 20)
            else:
                loop = False

        return option_input        


class World:
    def __init__(self, file_population, file_borders, file_airports,
                 file_ramdom_airports):
        self.file_population = file_population
        self.file_borders = file_borders
        self.file_airports = file_airports
        self.file_ramdom_airports = file_ramdom_airports
        self.countries = LinkedList()
        self.names = LinkedList()
        self.cure_progress = 0.0
        self.cure_delivered = False
        self.infection_detected = False
        self.infection_detection_day = 0
        self.actions_queue = LinkedQueue()
        self.infection = None
        self.day = 0
        self.closed_airports_today = ""
        self.closed_fronteirs_today = ""
        self.gave_masks_today = ""
        # sum of the new infected every day
        # It does not include the healing process
        self.infected_to_this_day = 0
        self.infected_per_day_list = LinkedList(1)
        self.dead_per_day_list = LinkedList(0) 

    @property
    def infected_total(self):
        inf = 0
        for country in self.countries:
            inf += country.infected_total
        return inf

    @property
    def healthy_total(self):
        h = 0
        for country in self.countries:
            h += country.healthy_total
        return h

    @property
    def dead_total(self):
        dead = 0
        for country in self.countries:
            dead += country.dead_total
        return dead

    @property
    def alive_total(self):
        alive = 0
        for country in self.countries:
            alive += country.alive_total
        return alive

    @property
    def initial_population(self):
        initial = 0
        for country in self.countries:
            initial += country.initial_population
        return initial

    @property
    def prob_detect_infection(self):
        p = (self.infection.visibilidad * self.infected_total * self.dead_total**2) / self.initial_population**3
        return p

    @property
    def prob_die(self):
        a = max(0.2, self.day**2 / 100000)
        p = min(a * self.infection.tasa_mortalidad, 1)

        return p

    @property
    def condition_spread_air(self):
        return self.infected_total >= 0.04 * self.initial_population

    def simulate_infection_detection(self):
        '''Simulates the bernoulli event of detecting the infection'''
        x = bernoulli(self.prob_detect_infection)
        if x == 1:
            self.infection_detected = True
            self.infection_detection_day = self.day

    def simulate_cure_progress(self):
        '''Simulates the cure progress in one day
        If the cure is completely researched, then it is delivered'''
        if self.infection_detected and not self.cure_delivered:
            self.cure_progress += self.healthy_total / (2 * self.initial_population * 100)

        if self.cure_progress >= 1 and not self.cure_delivered:
            random_country = choice(self.countries)
            random_country.has_cure = True
            self.cure_delivered = True

    def add_country(self, country):
        '''It checks if the country is already in the list.
        If not, then appends it'''
        if self.countries.find_name(country.name) is None:
            self.countries.append(country)
            self.names.append(country.name)

    def load_countries_csv(self):
        '''Reads and loads the borders.csv file'''
        with open(self.file_population) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            header = next(readCSV)
            for row in readCSV:
                name = str(row[0])
                population = int(row[1])
                country = Country(name, population)
                self.add_country(country)

    def load_neighbours(self):
        with open(self.file_borders) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=";")
            header = next(readCSV)
            for row in readCSV:
                country_name_1 = row[0]
                country_name_2 = row[1]
                country_1 = self.countries.find_name(country_name_1)
                country_2 = self.countries.find_name(country_name_2)
                country_1.add_neighbour(country_2)

    def load_air_neighbours(self):
        with open(self.file_ramdom_airports) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            header = next(readCSV)
            for row in readCSV:
                country_name_1 = row[0]
                country_name_2 = row[1]
                country_1 = self.countries.find_name(country_name_1)
                country_2 = self.countries.find_name(country_name_2)
                country_1.add_air_neighbour(country_2)

    def simulate_goverment_decitions(self):
        '''It simulates the three actions per day. It clears
        the list every day.'''
        self.closed_fronteirs_today = ""
        self.closed_airports_today = ""
        self.gave_masks_today = ""

        if self.infection_detected:
            # sorted_forbidden = sorted(self.actions_queue, reverse=True)
            # sorted_nice = LinkedList(*sorted_forbidden)
            sorted_nice = self.actions_queue.sorted()
            for i in range(min(3, len(self.actions_queue))):
                to_do = sorted_nice.pop_left()
                if to_do.message == 'close fronteirs' and to_do.origin.open_fronteir:
                    to_do.origin.open_fronteir = False
                    print("{} hizo: {}".format(to_do.origin.name, to_do.message))
                    for action in to_do.origin.actions_queue:
                        if action.message == to_do.message:
                            to_do.origin.actions_queue.remove(action)
                    self.closed_fronteirs_today += str(to_do.origin.name) + "\n\t\t"
                elif to_do.message == 'open fronteirs' and not to_do.origin.open_fronteir:
                    to_do.origin.open_fronteir = True
                    for action in to_do.origin.actions_queue:
                        if action.message == to_do.message:
                            to_do.origin.actions_queue.remove(action)                    
                    print("{} hizo: {}".format(to_do.origin.name, to_do.message))                    
                elif to_do.message == 'close airports' and to_do.origin.open_airport:
                    to_do.origin.open_airport = False
                    for action in to_do.origin.actions_queue:
                        if action.message == to_do.message:
                            to_do.origin.actions_queue.remove(action)                    
                    print("{} hizo: {}".format(to_do.origin.name, to_do.message))                    
                    self.closed_airports_today += str(to_do.origin.name) + "\n\t\t"
                elif to_do.message == 'open airports' and not to_do.origin.open_airport:
                    to_do.origin.open_airport = True
                    for action in to_do.origin.actions_queue:
                        if action.message == to_do.message:
                            to_do.origin.actions_queue.remove(action)                   
                    print("{} hizo: {}".format(to_do.origin.name, to_do.message))                    
                elif to_do.message == 'give masks' and not to_do.origin.has_mask:
                    to_do.origin.has_mask = True
                    for action in to_do.origin.actions_queue:
                        if action.message == to_do.message:
                            to_do.origin.actions_queue.remove(action)                  
                    print("{} hizo: {}".format(to_do.origin.name, to_do.message))             
                    self.gave_masks_today += str(to_do.origin.name) + "\n\t\t"

        self.closed_airports_today = self.closed_airports_today.strip()
        self.closed_fronteirs_today = self.closed_fronteirs_today.strip()
        self.gave_masks_today = self.gave_masks_today.strip()

        self.actions_queue.clear()

    def simulate_one_day(self):
        condition_spread_air = self.condition_spread_air
        world_infected_this_day = 0
        world_dead_this_day = 0

        self.day += 1
        self.simulate_cure_progress()
        for country in self.countries:
            country.simulate_one_day(self.infection, self.prob_die)
            country.simulate_spread_land()
            if condition_spread_air:
                country.simulate_spread_air()
            country.simulate_share_cure()
            country.simulate_propose(self.cure_progress >= 1, self.actions_queue)
            world_infected_this_day += country.infected_this_day
            world_dead_this_day += country.dead_this_day
        self.simulate_infection_detection()
        self.simulate_goverment_decitions()

        self.infected_to_this_day += world_infected_this_day
        self.dead_per_day_list.append(world_dead_this_day)
        self.infected_per_day_list.append(world_infected_this_day)

    def show_global_status(self):
        s_infected = "INFECTADOS: \n"
        s_clean = "LIMPIOS: \n"
        s_dead = "MUERTOS: \n"
        for country in self.countries:
            if country.status == 'Limpio':
                s_clean += "\t" + str(country.name) + "\n"
            elif country.status == 'Infectado':
                s_infected += "\t" + str(country.name) + "\n"
            elif country.status == 'Muerto':
                s_dead += "\t" + str(country.name) + "\n"

        print(s_clean)
        print(s_infected)
        print(s_dead)

        print("Poblacion total:")
        print("\t Viva: {}".format(self.alive_total))
        print("\t Muerta: {}".format(self.dead_total))
        print("\t Infectada: {}".format(self.infected_total))
        print("\t Sana: {}".format(self.healthy_total))

    def show_day_summary(self):
        world_infected_this_day = 0
        world_dead_this_day = 0
        for country in self.countries:
            world_infected_this_day += country.infected_this_day
            world_dead_this_day += country.dead_this_day

        print("Sucesos del DIA: ")
        print("\t Gente INFECTADA: {}".format(world_infected_this_day))
        print("\t Gente MUERTA: {}".format(world_dead_this_day))
        print("\t Aeorpuertos cerrados: \n\t\t" + str(self.closed_airports_today))
        print("\t Fronteras cerradas: \n\t\t" + str(self.closed_fronteirs_today))
        print("\t Mascarillas entregadas: \n\t\t" + str(self.gave_masks_today))

    def show_country_status(self):
        loop = True
        while loop:
            country_input = input("Nombre del pais: ").strip().title()
            country = self.countries.find_name(country_input)
            if country is None:
                print("Pais invalido. Intenta nuevamente.")
            else:
                loop = False
        print(country.name)
        print("\t Personas VIVAS: {}".format(country.alive_total))
        print("\t Personas INFECTADAS: {}".format(country.infected_total))
        print("\t Personas MUERTAS: {}".format(country.dead_total))
        print("\t Aciones propuestas no realizadas: {}".format(country.actions_queue))

    def show_averages(self):
        death_average = self.dead_total / self.day if self.day != 0 else 0
        infected_average = self.infected_to_this_day / self.day if self.day != 0 else 1

        print("Promedio de muertes diarias \t: {}".format(death_average))
        print("Promedio de infectados diarios \t: {}".format(infected_average))

    def show_dead_infected_per_day(self):
        # print("DIA \t | MUERTOS \t\t | INFECTADOS")
        # for i in range(self.day + 1):
        #   dead = self.dead_per_day_list[i]
        #   infected = self.infected_per_day_list[i]
        #   print(str(i) + "\t\t |" + str(dead) + "\t\t\t\t |" + str(infected))
        # print("-" * 25)
        infected_list = [num for num in self.infected_per_day_list]
        infected = np.array(infected_list)
        time = np.arange(0, self.day + 1)

        plt.plot(time, infected)
        plt.title('Infected per day')
        plt.ylabel('Infected')
        plt.xlabel('Day')

        plt.show()


class Country:
    def __init__(self, name, initial_population):
        self.name = name
        self.initial_population = initial_population
        self.healthy_total = initial_population
        self.dead_total = 0
        self.infected_total = 0
        self.actions_queue = LinkedList()
        self.neighbours = LinkedList()
        self.neighbours_names = LinkedList()
        self.air_neighbours = LinkedList()
        self.air_neighbours_names = LinkedList()
        self.open_airport = True
        self.open_fronteir = True
        self.has_cure = False
        self.has_mask = False
        self.infected_this_day = 0
        self.dead_this_day = 0

    @property
    def alive_total(self):
        '''Returns the total amount of living people'''
        return self.healthy_total + self.infected_total

    @property
    def status(self):
        '''Returns the state of a country as a string'''
        s = None
        if self.infected_total == 0:
            s = "Limpio"
        elif self.infected_total > 0:
            s = "Infectado"
        if self.dead_total == self.initial_population:
            s = "Muerto"
        return s

    @property
    def neighbours_available(self):
        '''Returns list with neighbours with opened fronteir'''
        n_a = LinkedList()
        for neib in self.neighbours:
            if self.open_fronteir and neib.open_fronteir:
                n_a.append(neib)
        return n_a

    @property
    def air_neighbours_available(self):
        '''Returns a list with neighbours with open airport'''
        a_n_a = LinkedList()
        for neib in self.air_neighbours:
            if self.open_airport and neib.open_airport:
                a_n_a.append(neib)
        return a_n_a

    @property
    def prob_spread_land(self):
        '''Returns the probability of spreading the infection by land'''
        try:
            num_conections = len(self.neighbours_available)
            p = min(0.07 * self.infected_total / (self.alive_total * num_conections), 1)
        except ZeroDivisionError:
            return False
        else:
            return p

    @property
    def prob_spread_air(self):
        '''Returns the probabily of infection by air'''
        try:
            num_conections = len(self.air_neighbours_available)
            p = min(0.07 * self.infected_total / (self.alive_total * num_conections), 1)
        except ZeroDivisionError:
            return False
        else:
            return p

    def add_neighbour(self, other):
        '''Checks if the two countries are already connected and adds them to each other lists'''
        if other.name not in self.neighbours_names:
            self.neighbours.append(other)
            self.neighbours_names.append(other.name)

        if self.name not in other.neighbours_names:
            other.neighbours.append(self)
            other.neighbours_names.append(self.name)

    def add_air_neighbour(self, other):
        '''Checks if the two countries are already connected and
        adds them to each other lists. This one is by air.'''
        if other.name not in self.air_neighbours_names:
            self.air_neighbours.append(other)
            self.air_neighbours_names.append(other.name)

        if self.name not in other.air_neighbours_names:
            other.air_neighbours.append(self)
            other.air_neighbours_names.append(self.name)

    def simulate_one_day(self, infection, prob_die):
        '''It simulates the actions of one day. First they can
        cure themselves, then they infect other people and finally
        they can die. This order makes sense to me'''
        if self.status == "Infectado":
            if self.has_cure:
                p = 0.25 * infection.resistencia_medicina
                if self.infected_total >= 1000:
                    sample = int(str(self.infected_total)[0:3])
                    x = sum(bernoulli(p) for i in range(sample)) / sample
                    new_cured = round(x * self.infected_total)
                    for i in range(new_cured):
                        self.cure_one()
                else:
                    for i in range(self.infected_total):
                        x = bernoulli(p)
                        if x == 1:
                            self.cure_one()

            if self.infected_total >= 1000:
                sample = int(str(self.infected_total)[0:3])
                u_prom = sum(uniform() for i in range(sample)) / sample
                n = round(u_prom * infection.tasa_contagiosidad)
                if self.has_mask:
                    n *= 0.3
                new_infected = round(n * self.infected_total)
                self.infect_one(new_infected)
                self.infected_this_day = min(new_infected, self.healthy_total)
            else:
                self.infected_this_day = 0
                for i in range(self.infected_total):
                    u = uniform()
                    n = u * infection.tasa_contagiosidad
                    if self.has_mask:
                        n *= 0.3
                    self.infect_one(int(n))
                    self.infected_this_day += min(int(n), self.healthy_total)

            if self.infected_total >= 1000:
                sample = int(str(self.infected_total)[0:3])
                x = sum(bernoulli(prob_die) for i in range(sample)) / sample
                new_dead = round(x * self.infected_total)
                self.kill_one(new_dead)
                self.dead_this_day = min(new_dead, self.infected_total)
            else:
                self.dead_this_day = 0
                for i in range(self.infected_total):
                    x = bernoulli(prob_die)
                    if x == 1:
                        self.kill_one()
                        self.dead_this_day += min(1, self.infected_total)

    def simulate_spread_land(self):
        '''Simulates the event of infecting other country by land'''
        if self.infected_total >= 0.2 * self.initial_population:
            for country in self.neighbours_available:
                if country.status == 'Limpio':
                    p = self.prob_spread_land
                    x = bernoulli(p)
                    if x == 1:
                        country.infect_one()

    def simulate_spread_air(self):
        '''Simulates the event of infecting other country by air.
        This does not includes the 4 percent condition'''
        for country in self.air_neighbours_available:
            if country.status == 'Limpio':
                p = self.prob_spread_air
                x = bernoulli(p)
                if x == 1:
                    country.infect_one()

    def simulate_share_cure(self):
        '''It gives the cure to the countries with open airport'''
        if self.has_cure:
            for country in self.air_neighbours_available:
                if not country.has_cure:
                    country.has_cure = True

    def add_proposal(self, proposal_object, world_actions_queue):
        found_another = False
        replace = False
        for action in self.actions_queue:
            if action.message == proposal_object.message:
                found_another = True
                if proposal_object.priority > action.priority:
                    replace = True
                    self.actions_queue.remove(action)
        if not found_another:
            self.actions_queue.append(proposal_object)
        if replace:
            self.actions_queue.append(proposal_object)

        world_actions_queue.append(proposal_object)

    def simulate_propose(self, cure_discovered, world_actions_queue):
        '''It simulates the gobernment decitions on a day'''
        ratio = self.infected_total / self.initial_population

        if (self.infected_total > self.initial_population / 2 or self.dead_total >= self.initial_population / 4) and\
         self.open_fronteir and not cure_discovered:
            action = 0
            for country in self.neighbours:
                action += country.infected_total / country.initial_population
            if len(self.neighbours) != 0 and action != 0:
                action /= len(self.neighbours)
                priority = action * ratio
                proposal_msg = 'close fronteirs'
                proposal_object = Proposal(priority, proposal_msg, self)
                self.add_proposal(proposal_object, world_actions_queue)
                # world_actions_queue.append(proposal_object)

        if (self.infected_total > 0.8 * self.initial_population or self.dead_total > 0.2 * self.initial_population) and\
         self.open_airport and not cure_discovered:
            action = 0.8
            priority = action * ratio
            proposal_msg = 'close airports'
            proposal_object = Proposal(priority, proposal_msg, self)
            self.add_proposal(proposal_object, world_actions_queue)
            # world_actions_queue.append(proposal_object)

        if self.infected_total > self.initial_population / 3 and not self.has_mask:
            action = 0.5
            priority = action * ratio
            proposal_msg = 'give masks'
            proposal_object = Proposal(priority, proposal_msg, self)
            self.add_proposal(proposal_object, world_actions_queue)
            # world_actions_queue.append(proposal_object)

        if ((self.infected_total <= self.initial_population / 2 and
                self.dead_total < self.initial_population / 4) and
                not self.open_fronteir) or (cure_discovered and not self.open_fronteir):
            action = 1 if cure_discovered else 0.7
            priority = action * ratio
            proposal_msg = 'open fronteirs'
            proposal_object = Proposal(priority, proposal_msg, self)
            self.add_proposal(proposal_object, world_actions_queue)
            # world_actions_queue.append(proposal_object)

        if ((self.infected_total <= 0.8 * self.initial_population and
                self.dead_total <= 0.2 * self.initial_population) and
                not self.open_airport) or (cure_discovered and not self.open_airport):
            action = 1 if cure_discovered else 0.7
            priority = action * ratio
            proposal_msg = 'open airports'
            proposal_object = Proposal(priority, proposal_msg, self)
            self.add_proposal(proposal_object, world_actions_queue)
            # world_actions_queue.append(proposal_object)

    def infect_one(self, num=1):
        if self.healthy_total >= num:
            self.infected_total += num
            self.healthy_total -= num
        else:
            new_infected = self.healthy_total
            self.infected_total += new_infected
            self.healthy_total -= new_infected

    def kill_one(self, num=1):
        if self.infected_total >= num:
            self.dead_total += num
            self.infected_total -= num
        else:
            new_dead = self.infected_total
            self.dead_total += new_dead
            self.infected_total -= new_dead

    def cure_one(self, num=1):
        if self.infected_total >= num:
            self.healthy_total += num
            self.infected_total -= num
        else:
            new_cured = self.infected_total
            self.healthy_total += new_cured
            self.infected_total -= new_cured

# Main
generate_connections()
world = World("population.csv", "borders.csv", "airports.csv",
              "random_airports.csv")
world.load_countries_csv()
world.load_neighbours()
world.load_air_neighbours()
g = Game(world)

print("""*******************************************************
***                                                 ***
***              Bienvenido a Pandemic IIC          ***
***                                                 ***
*******************************************************""")
print("------------------------------------------------------")

print("Bienvenido a Pandemic, en este juego podras \n\
destruir a toda la humanidad c:")

g.choose_infection()
g.choose_country()
loop = True
while loop:
    if g.world.infected_total == 0:
        print()
        print("Ya no quedan mas infectados en el mundo")
        print("No has podido destruir a la humanidad")
        break
    elif g.world.alive_total == 0:
        print()
        print("Ya no quedan mas vivos en el mundo")
        print("Has destruido a la humanidad")
        break
    option = g.main_menu()
    if option == 1:
        g.world.simulate_one_day()
    elif option == 2:
        statistics_op = g.statistics_menu()
        if statistics_op == 1:
            g.world.show_country_status()
        elif statistics_op == 2:
            g.world.show_global_status()
        elif statistics_op == 3:
            g.world.show_averages()
        elif statistics_op == 4:
            g.world.show_day_summary()
        elif statistics_op == 5:
            g.world.show_dead_infected_per_day()
        elif statistics_op == 6:
            continue
    elif option == 3:
        print("Aun no implementado")
    elif option == 4:
        print("Gracias por jugar")
        loop = False

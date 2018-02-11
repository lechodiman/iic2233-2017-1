# README T02

Los archivos para esta entrega son :
    - bernoulli_event. py
    - linked_lists. py
    - menu. py
    - proposal. py

El archivo principal es menu.py. La mayoría de los métodos y funciones que no son obvios vienen con un docstring en inglés. De paso pido perdón si tengo alguna falta gramatical al escribir los docstrings en inglés. 

# NO implementado
Lo que no alcancé a implementar fue:
    - Guardar estado de un juego.
    - Cargar estado de un juego guardado previamente.

# Carpeta Diagrama Clases
En esta carpeta está el diagrama de clases preliminar (subido al SIDING), es aproximadamente un 70% igual al cógido implementado finalmente.

# bernoulli_event .py
Contiene funciones para simular una variable que distribuya uniforme entre (a,b) o que distribuya según un evento bernoulli, es decir, que tome el valor 1 con p de probabilidad, y 0 con (1-p) de probabilidad.

# proposal. py
Define la clase __Proposal__ que servirá para instanciar las diversas acciones que los paises decidan tomar.
Recibe un prioridad (que es redondeada a 4 digitos), un mensaje (qué desea hacer el páis) y el país de origen (instancia de clase Country)
Se define un método __repr__ para poder representarlas de mejor forma.
Se define el método __lt__ para poder ordenarlas según algún algoritmo de ordenación.

# linked_lists. py
En este modulo defino las EDD que usé en la T02.

__Node__:
Un nodo posee un atributo 'data' que puede ser de cualquier tipo, y una referencia al siguiente nodo en caso de que exista.
__LinkedList__:
Es la EDD que más sobre exploté en la Tarea.Posee 'head' que referencia al primer nodo, 'tail' que referencia al último nodo (útil para hacer append al final de la lista), y posee 'size' para definir el método len().
Se puede instancia recibiendo *args, los cuales serán por defecto agregados en el orden en que se entreguen.

- pop_left: Retorna el primer elemento de la lista y lo retira de esta.
- append_left: Agrega un elemento al comienzo de la lista.
- append: El viejo y confiable append de las listas por defecto.
- remove: El otro viejo y confiable remove de las listas.
- find: Busca un elemento de la lista y lo retorna si existe, retorna None en otro caso.
- find_name: Nuevo método que funciona cuando los elementos de una lista tienen atributo 'name'. Recibe un 'name' y retorna el objeto con ese 'name' si lo encuentra. Retorna None en otro caso.
- in: El típico método para que los bool de tipo 'element in list' funcione.
- len: Retorna el valor de 'size'.
- iter: Generador que yields el valor de un nodo en la lista.
- repr: Printea la lista como las listas por defecto de Python.
- getitem: Para que funcione la indexacion.
- clear: Remueve todos los elementos de la lista.
- count: Recibe un elemento y retorna el numero de veces que se encuentra en la lista.

__LinkedQueue__:
Hereda de LinkedList, por lo que comparte todos sus métodos y atributos.
Le incorporé el método sort_append y sorted.
- sort_append: Agrega los elementos ordenados de mayor a menor (útil para ordenar por prioridad)
- sorted: Retorna una LinkedQueue con todos sus elementos ordenados según sort_append

# menu .py
Modulo principal para el juego. Importo las EDD creadas en linked_lists.py, la función generate_connections, ABCMeta para definir clases abstractas, las funciones bernoulli y uniform para simular variables aleatorias, la clase Proposal, choice from random (para seleccionar un país aleatorio al entregar la cura) y el módulo csv (para cargar los datos del enunciado).

__Infection__:
Clase abstracta para definir el 'name' de la infection.

__Virus__, __Bacteria__ y __Parasite__:
Heredan de infection, poseen atributos fijos de sus distintas tasas.

__Country__:
Posee 'name', 'initial_population' y atributos para contar la cantidad de infectados, muertos, vivos y sanos del país.Por defecto todos los paises tiene atributo 'open_airport' = True, por lo que asumo que todos los paises tienen aeropuerto. Solo los paises que tengan conexiones con otros países (por aire) podrán usar su aeropuerto.

- actions_queue: Lista para almacenar las acciones que el país quiere tomar pero aun no han sido implementadas.
- neighbours, air_neighbours: Listas para almacenar a los vecinos por tierra y por aire respectivamente.
- neighbours_names, air_neighbours_name: Listas con los nombres de los paises vecinos por tierra y por aire respectivamente
- open_airport, open_fronteir, has_cure, has_mask: Variables booleanas que indican si un pais tiene su aeropuerto abierto, frontera abierta, tiene la cura o ha repartido máscaras.
- infected_this_day : contador que se actualiza por dia, indica la cantidad de personas infectadas al avanzar un día.
- dead_this_day: ídem a la variable anterior.

Todos los métodos y properties vienen con su docstring explicativo.
Cabe mencionar que al simular el avance de la infeción dentro del país (simulate_one_day()), si la cantidad de infectados es mayor a 1000, se tomará una muestra de máximo 999 para agilizar la simulación.

El método que no contiene docstring es add_proposal dado que fue uno de los últimos implementados. Este método recibe un objeto de tipo Proposal y lo agrega a la cola del país solo si no hay otro del mismo tipo o su prioridad es más alta. Tambíen se agrega a la cola del mundo.

__World__:
Posee los nombres de los archivos para cargar paises y conexiones entre ellos.
- countries, names: listas que contienen los paises y los nombres de estos respectivamente.
- cure_progress, cure_delivered: la primera indica el porcentaje de progreso de la cura y la segunda es un bool que indica si la cura fue entregada o no.
- infection_detected, infection_detection_day: la primera es un bool que indica si la infección ya fue detectada o no. La segunda registra el día en que esta fue detectada.
- actions_queue: LinkedQueue que contiene las Proposal de todos los países del mundo. Se vacía cada día.
- infection: Contiene la instancia de Infection que se usará en el juego.
- day: número que indica el día actual en el juego
- closed_airports_today, closed_fronteirs_today, gave_masks_today: son strings que contienen el nombre de los países que hicieron cierta acción en el día. Se reinicia cada vez que se llama al método show_day_summary.
- infected_to_this_day: variable que suma la cantidad de infectados por día, si alguien se cura no se resta a esta variable. Es para calcular el promedio de infecciones.
- infected_per_day_list, dead_per_day_list: listas que contiene la cantidad de infectados y muertos por día.

Métodos:
- simulate_one_day: Verifico la condicion de contagio por aire. Primero se simula el progreso de cura (los científicos son los primeros en despertar). Luego en cada país se simula el avance de la enfermedad en el país, a otro país por tierra, a otro país por aire, se comparte la cura a otros países y finalmente el gobierno de cada país envía sus propuestas al mundo. Al final de día (en las noticias) se verifica si la infección se ha descuebierto y se simulan las desiciones del gobierno mundial.
- show_global_status: Imprime el estado del mundo
- show_day_summary: Imprime el resumen del día
- show_country_status: Pide un country e imprime los datos de ese country
- show_averages: Imprime los promedios de muertes e infecciones por día
- show_dead_infected_per_day: Imprime de forma tabular la cantidad de muertos e infectados por día.

__Game__
Posee una referencia al mundo del juego.

Métodos:

- choose_infection: Setea el parámetro infection del mundo a la infección que escoja el usuario (y nombre de la infección)
- choose_country:Imprime nombres de los países y su population. Pide el nombre de un país e infecta a la primera persona en dicho país.
- main_menu: Imprime el menu principal del juego
- statistics_menu: Imprime el menú para escoger qué estadística desea ver el usuario.

# Main
Al comienzo del juego se generarán las conecciones aleatorias, se instancia el world, se cargan los paises, se generan las conexiones por tierra y por aire y se instacia el game recibiendo al world.
Luego se pide escoger la infección, escoger el país y se entra en un loop donde se imprime el main_menu y se ejecutan las funciones correspondientes.En el caso de la opción 3, se imprime que la opción de cargar juego no ha sido implementada (por esto tampoco se da la opción para guardar el game)








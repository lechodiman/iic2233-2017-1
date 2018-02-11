# README T04

Los archivos para esta entrega son :
    - bernoulli_event. py
    - t04. py
    - my_random. py

El archivo principal es t04 .py. La mayoría de los métodos y funciones que no son obvios vienen con un docstring en inglés. De paso pido perdón si tengo alguna falta gramatical al escribir los docstrings en inglés. A continueación explico brevemente los métodos, atributos y clases que no tienen docstring.

# NO implementado
Lo que no alcancé a implementar fue:
    - Implementación y carga de escenarios.csv
    - Implementación y carga de parámetros.csv
    - Evento ATRASO MAVRAKIS, DESCUENTO MAVRAKIS.
    - Evento EXAMEN tiene problemas para compilar.

# Diagrama de Eventos
Acá se encuentra el diagrama de eventos. Sin embargo, se me olvidó subirlo al cuestionario del SIDING. Cabe mencionar que el diagrama de eventos lo subí a github el día jueves (antes de la fecha límite).

# bernoulli_event .py
Contiene funciones para simular una variable que distribuya uniforme entre (a,b) o que distribuya según un evento bernoulli, es decir, que tome el valor 1 con p de probabilidad, y 0 con (1-p) de probabilidad.

# my_random. py
Contiene la función weighted_choice, esta fue obtenida de stackoverflow (https://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice). 

# t04 .py
__AdvancedProgramming__:
Posee un dicionario de secciones ({'1': Section(), ..., }), coordinador, ayudantes docentes (techer assistants), ayudantes de tareas (task assistants), lista de eventos (event list) y registros de las fechas donde se realiza una actividad o una tarea. Los demás atributos se explican con el nombre.

- all_students: Retorna una lista con todos los estudiantes del curso
- controles_week, corte_agua_weeks: Retornan una lista con las fechas cueando hay controles (o cortes de aguas) en semanas desde el inicio de la simulación.


__Section__:
Estructura que sirve para modelar una sección del curso.

- students: Lista de intancias de Student
- proffesor: Instancia de Proffesor.

Métodos:
- add_student: Añade alumno a la estructura
- add_proffesor: Asigna un profesor a la sección.

__Person__:
Clase base para definir un __repr__ y el nombre de una persona.

__Coordinator__:
Clase para instancia al Mavrakis.

__Proffessor__:
Clase para simular a los profesores.
- cola: Lista que almcenará a los alumnos que lo visiten

Métodos:
- atender_students(time_day, capacity): Recibe un dia para registrar en el alumno el día que fue atendido. Una capacidad para atender a los alumnos de la cola (fila). La elección se realiza de forma aleatoria.

__TeacherAssistant__:
Clase para simular a los ayudantes docentes.
- skilled_subjects: Es una lista con los números de las materias en las cuales el ayudante se destaca. Posee tres elementos.


__Student__:
- Student.nota_esperada: Es un diccionario en forma de dataframe que se utiliza para obtener la nota esperada dependiendo de las horas estudiadas.
- Student.dificulty: Lista con las dificultades de cada materia ordenada cronológicamente.
- horas_estudiadas, horas_tareas: Diccionario. Corresponde a las horas que efectivamente se dedicaron para cierta actividad. Se calcula desde 0 cada vez que se necesitan.
- manejo_contenidos: Diccionario ({contenido: valor}). 
- programming_levels_dict: Diccionario que almacena el nivel de programación de todas las semanas. Se actualiza al comenzar una cátedra.
- notas_exam, notas_act, notas_tareas, notas_controles: Diccionarios que almacenan el número de la semana en la cual se realizó la evaluación y la nota obtenida.
- catedra_help_days, tips_days, ayudantia_tips_days, party_days, meeting_days, football_days: Son listas que llevan registros de ciertos eventos que afectan en los parámetros de un estudiante.
- active: True si el alumno no ha botado el ramo, Falso en caso contrario.
- promedio: Retorna el promedio calculado con las notas publicadas del alumno.

Métodos:
- go_to_party(time_day): Añade la fecha a la lista correspondiente.


__Simulation__:
Clase pensada para controlar todas las simulaciones que se hagan y obtener las estadísticas.

Métodos:
- load(): Carga el archivo 'integrantes.csv' e instancia todas las clases correspondientes en la estructura correspontiente.
- get_global_statistics(): Imprime la cantidad de alumnos que botaron el ramo y la confianza promedio entre el inicio y el final del semestre.
- get_personal_statistics(): Pide el nombre del alumno como input e imprime sus estadisticas. Estas son: nivel programación promedio, confianza final, gráficos de Manejo de contenidos vs Semanas, imprime las notas de todas las evaluaciones que dió.
- get_grahps(): Muestra los gráficos de promedio de controles, tareas y actividades.


# main
Al comienzo de la simulación se cargará inmediatamente una instacia de Simulation y se leerá el archivo 'integrantes.csv', no considera 'escenarios.csv' o 'parametros.csv'.

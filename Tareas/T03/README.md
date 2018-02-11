# README T03

Los archivos para esta entrega son :
    - basic_commands. py
    - commands_data_return. py
    - consult_processing. py
    - main. py
    - my_csv .py
    - my_exceptions .py
    - my_math .py
    - my_types. py
    - my_tests .py

# NO implementado
Lo que no alcancé a implementar fue:
    - Función 'do_if' y su testing.
    - Que al guardar una columna como generador, esta pueda usarse muchas veces sin 'gastar' el generador. Sin embargo, si se guarda como lista, se puede utilizar la variable múltples veces.

# Idea general
La mayoría de las funciones toman los argumentos obvios y también reciben la instancia de una clase, para que puedan analizar si esta instancia posee algún atributo con cierto nombre. De esta forma puedo guardar variables como atributos de un objeto, en este caso, del objecto que es instancia de T03Window.

# basic_commands .py
Contiene funciones que corresponden a los comandos básicos. La función asignar se encuentra en el módulo 'consult_processing.py'
- generate_distribution(model_name, *args): Retorna una funcion de python, esperando para ser evaluada. Estas funciones pueden ser 'GAMMA', 'EXPONENTIAL', o 'NORMAL'. *args corresponde a los argumentos que recibirá la función de probabilidades, más la instancia de T03Window.
- graficar(column, option, o_instance): Utiliza la librería matplotlib y numpy para graficar una columna. Una columna debe ser un iterable pero no string. Option es un string que indica cómo graficarlo o puede ser una columna. Si option es un rango, según el formato definido en el enunciado, se llamará a la función 'to_range'. Si al finalizar de procesar todo, no se lanzan errores y se grafica, se retornará como output el string 'Graficando'.

# commands_data_return .py
Contiene las funciones que retornan valores o conjuntos de valores.
- get_column(file_name, column_name, o_instance): Retorna un generador con los valores correspondientes a la columna column_name, en el archivo file_name. Se utiliza os.path.isfile() para verificar que el archivo existe, de lo contrario se arroja una excepción. Para leer el archivo se utiliza la función reader del módulo 'my_csv'. Tambíen se verifica si en la columna existe aluna referencia a alguna variable guardada en el sistema.
- filtrar(column, symbol, value, o_instance) y operar(column, symbol, value, o_instance): Ambas funciones trabajan de manera similar. Se verifica si la columna o el value son valores que ya están guardados en el sistema. Se realiza una verificación de tipos. Y se retorna un generador de los valores 'filtrados' u 'operados'.
- evaluar(function, start, end, step, o_instance): Retorna un generador con los valores 'evaluados' en la funcion. Se realiza la verificación si es que function ya es una variable asignada en el sistema. Que sea, efectivamente, una función. Para retornar los valores se utiliza la función 'float_range'.
- LEN, PROM, DESV, VAR, MEDIAN (column, o_instance): Son funciones con comportamiento similar. Verifican si column es una variable ya asignada en el sistema y que sea un iterable pero no string. Finalmente, retornan el valor correspondiente.
- apply_command(column, command, o_instance): Esta funcion llama a las funciones estadísticas anteriores y retorna el valor entregado por el llamado. Si command no es una función implementada, arrojará un error. 
- comparar_columna(column_1, symbol, command, column_2, o_instance): Crean valores v_1 y v_2 que son el resultado de aplicar la funcion command sobre las columnas 1 y 2 respectivamente. Finalmente entrega el valor entregado por la función 'to_filter'.
- comparar(num_1, symbol, num_2, o_instance): Se realizan los chequeos de tipo. Finalmente se retorna el valor entregado por la función 'to_filter'.

# consult_processing .py
Módulo para definir la función asignar y unit_process_consult.
- asignar(var, value, o_instance): Setea en el objeto 'o_instance' una variable con el nombre contenido en var y con el valor value. Este valor no puede tener el nombre de una función del sistema. Retorna el string 'asignar' como output.
- unit_process_consult(consult, o_instance): Retorna el valor obtenido al evaluar la consulta. Consult debe ser un string con el formato de las consultas. Se revisa si hay alguna lista dentro de la consulta, si la hay se 'reemplaza' por el valor de esa consulta anidada, llamando a la función 'unit_process_consult' nuevamente. 
- class A: Esta clase está demás (perdón por no sacarla :C), fue para probar las funciones en un objeto cualquiera.


# main .py
Modulo principal. Se sobreescribieron las funciones process_consult y save_file.

- process_consult(self, querry_array): No retorna nada. Se procesa cada una de las consultas, llamando a unit_process_consult. Si se generan errores, estos se muestran en la interfaz según el formato especificado.
- save_file(self, querry_array): Funciona de manera similar a process_consult, sin embargo, esta en vez de mostrar los resultados en pantalla, los guarda en un archivo 'resultados.txt'.

# my_csv .py
Simula el viejo y confiable módulo csv de python.
- reader(file_object, delimiter): Retorna un generador con las filas de un archivo, separadas según delimiter.

# my_exceptions. py
Se crean las excepciones que controlará el programa. Básicamente, sobreescribí el método __str__ para que imprima la causa del error según corresponda.

# my_math .py
Creo mis propias funciones sqrt y factorial que simulan a las del módulo math.

# my_types .py
En este módulo creo funciones auxiliares que me ayudan a que las demás funciones tengan menos código repetido.
- is_iterable(thing): Retorna True si thing es iterable pero no string, False en otro caso.
- is_number(s): Retorna True si s es un int o float o string que puede ser transformado a uno de los tipos mencionados.
- float_range(x, y, step=1.0): Simula al viejo y confiable range de Python pero este está con esteroides y puede trabajar con floats. Retorna el rango como un generador.
- to_range(range_str): Recibe un string de rango en el formato especificado en el enunciado. Lo transforma a un rango con ayuda de float_range.
- to_filter(symbol, value) y to_operation(symbol, value): Funcionan de manera similar. Retornan una función. En el caso de to_filter, esta retorna True si al evaluarla cumple la condición dada por symbol y value. En el caso de to_operation, esta retorna el valor al evaluar su argumento con value de acuerdo a symbol.

# my_tests.py
En este módulo realizo los tests para las funciones con unittest.

- class AwesomeWindow: Es solo para simular a la clase T03Window y poder guardar variables como atributos de la instancia.
- class SuperThing: Es solo para verificar que si guardo una instancia de esta clase como variable dentro de AwesomeWindow, puedo acceder a la misma instancia guardad.

- test_prom, test_len, test_desv, test_median, test_var: Funcionan de forma similar. Testeo una igualdad segura. Errores que pueden arrojar las funciones. Error de asignación. Y luego agrego la variable en la instancia de AwesomeWindow, para testear lo mismo pero que no arroje error. Finalmente deleteo el tributo 'x'.
- test_asignar: Creo una instancia de una clase cualquiera (SuperThing), para usar la funcion asignar y verificar que esta funciones bien. Tambíen verifico que no pueda guardar una variable con el nombre de alguna función.
- test_filtrar, test_evaluar: Funcionan casi igual. Se testea una igualdad segura, una referencia inválida, y se prueba que al asignar variable en AwesomeWindow, estas pueden ser accedidas correctamente.
- test_comparar_columna: Testeo una igualdad simple y que efectivamente lance el error argumento invalido si se llama con un argumento que no existe.
- test_error_matematico y test_argumento_invalido: son para testear los errores que no fueron testeados por las funciones anteriores. Se verifica el error matemático al intenar evaluar una Normal(0, 0) o una Gamma(-1, 1). Se verifica el test de argumento inválido al pasar un argumento extra en la asignacion de una función de probabilidad.


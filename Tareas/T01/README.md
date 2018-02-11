# README T01

# functions.py
En este modulo se encuentran funciones auxiliares para la maniupulacion de ubicaciones y años:

  - intersect: retorna True si dos circulos se intersectan, False eoc.
  - is_bisiesto: retorna True si el año es bisiesto, False eoc.
  - grados_a_puntos: pasa de una tupla en grados, a una tupla en puntos en un plano
  - dist_entre_grados: calcula la distancia en km entre puntos de la forma (lat, lon)

# classes.py
Contiene las clases utilizadas y las funciones que cargan las bases de datos.

  - leer_db: retorna una lista con los objetos respectivos de una base de datos
  - leer_db_usuarios: retorna una lista con los usuarios (instanciados) dependiendo de su cargo

# MiFecha
Clase para manipular las fechas dentro del programa
- __lt__: Para comparar si una fecha es menor a otra
- __sub__: Retorna la diferencia en minutos entre dos fechas
- __eq__: Retorna True si dos fechas tienen los mismos atributos
- sumar_segundos: Permite actualizar los atributos de una instancia si se le aumentan los segundos transcurridos
- copy: Retorna un objeto de tipo MiFecha con los mismos atributos de la instancia (sirve para guardar fechas en distintas variables y luego actualizar una y que la otra no se afecte)
- __str__: Imprime la fecha en el formato que aparece en los csv
- __from_str__: Metodo de clase que instancia un objeto  a partir de un string con el formato que aparece en los csv.

# Incendio
De aca en adelante todas las clases tendran un metodo de clase llamado from_dict que instancia un objeto a partir de un diccionario con los atributos de cada clase.

Clase para instanciar los incendios, posee los atributos obvios que aparecen en los csv y ademas:

- puntos_poder_extintos: registro de los puntos de poder que se extinguieron
- recursos_utilizados : lista con Recursos que actuaron
- fecha_cese : None por defecto, debe ser un objeto MiFecha cuando no sea None
- recursos_trabajando: lista con los recursos actualmente trabajando (no fue implementado al final)
- porcentaje_ext: 
- activo: retorna True si pp > 0, False eoc.
- puntos_poder: posee la definicion de pp
- suerficie_afectada: idem a lo anterior


Metodos de Incendio
- hay_nubes: recibe una fecha actual y una altura. Retorna True si hay nubes a mayor altura de la altura ingresada en dicha fecha.
- simular: Dependiendo de la fecha actual, simula el radio del incendio a partir de las condiciones meteorologicas a las que se ve afectado. Revisa por minuto, por lo que se demora al calcular (pero lo hace).
- str: Imprime el incendio bonito.
- recibir_recurso: Reduce los puntos de poder por el efecto de un recurso actuando. Sin embargo, no recalcula los puntos de poder durante el tiempo que actua el recurso (efecto meteorologico) :C

# Recurso
Ademas de lo basico, tiene:
- tiempo_trabajado: no implementado
- dist_a_objetivo: no implementado
- inc_trabajados: lista con Incendios donde ha trabajado el Recurso.
- techo: techo de nubes que 'soporta' un avion o helicoptero, si no es de tipo avion o helicoptero, el techo es un numero muy grande.
- fechas_salidas : contiene tuplas de la forma (f salida, f llegada, f retirada, f regreso) 
- estado_actual: actualiza el estado según la fecha actual. Revisa si la fecha está entre f salida, f llegada, f retirada, f regreso.
- ubicacion_actual: "en ruta a incendio" y "en ruta a base" no fueron implementados.

Metodos de Recurso:

-enviar_a_incendio: Revisa si hay nubes en caso de un recurso volador, si hay no lo envia. Registra al incendio como incendio trabajado. Calcula el tiempo de viaje y registra las fechas respectivas.
-__str__: Imprime toda la info importante del recurso
__repr__: Version mucho mas resumida de lo anterior, es para que cuando un Incendio imprima los recursos que estan trabajando, no imprima un mensaje gigante.

# Meteorologia
No tiene nada del otro mundo, solo lo necesario que viene en los csv.

Metodos de Meteorologia:
- __str__: Imprime la info bonita de un reporte meteorologico
- __lt__: Un reporte es menor a otro si su respectiva fecha de inicio lo es.

# Usuario
Super clase para los distintos tipos de usuarios. Tiene los atributos obvios, el viejo y confiable from_dict y un __str__ loco para que se vean lindo.

# UsuarioANAF
Igual al padre.

# Piloto y Jefe
Contienen una var booleana para ver si fueron asignados o no a un incendio.

# menu.py

Modulo con todas las funciones para que funcione el menu. Al final del modulo se lanza el menu.

__Funciones__:
- first_menu, hora, fecha : Estos tipos sirven para pedir el input de usuario, hora y fecha respectivamente. Retornan una tupla con (True si hubo error, argumentos de interes). La variable booleana del comienzo es para que al introducir en un loop, este se mantenga hasta un ingreso correcto del usuario.
- set_hora_fecha, set_user: Funciones que llaman a las anteriores para setear una fecha y un usuario (retornarlos y guardarlos en variables).
- menu_ANAF, menu_P_J: Imprimen lo que tienen que imprimir C:
- desplegar_base_(incendios, recurso, usuario, meteorologia): Para desplegar incendios y recursos se pide un id especifico, ya que en caso contrario habria que simular todo y se demoraria mucho. Para usuarios y meteorologia los imprime todos.
- agregar_(incendios, recurso, usuario, meteorologia): Usan diccionarios para saber el orden de las columnas y luego agregar la nueva linea en el mismo orden de las anteriores.
- leer_info_incedio: Recibe un usuario y revisa si este fue asignado al incendio, si lo fue imprime la info del incendio. No lo hace en otro caso.
- leer_info_recurso: Recibe un usuario e imprime la info conrrespondiente a su recurso.
- desplegar_incendios_(activos, apagados): Estas funciones revisan si el incendio esta activo o apagado en una cierta fecha. Para esto simulan los puntos de poder.
- desplegar_rec_(utilizados, efectivos) : No implementadas

Finalmente viene el menu propiamente tal:

__OOH NO!!__ Haciendo el README me acabo de dar cuenta que en el commit que envie tengo comentada la parte donde pide la fecha y puse una como 'por defecto' para que al probar el programa no tenga que ingresar la fecha una y otra ves. De todas formas si se 'descomenta' el programa funciona perfectamente. 

dict_options(ANAF, P_J) son diccionarios con las funciones que mencioné anteriormete para llamarlas facilmente.

El resto es solo control de flujo para manejar la interfaz que ve el usuario.

# Diagrama de clases

Debido a que tuve un problema con el internet al momento de hacer el commit con el diagrama, no alcancé a cambiarle nombre.

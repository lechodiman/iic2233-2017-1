# README T05


El archivo principal es main .py.

# NO implementado
Lo que no alcancé a implementar fue:
- Funcionalidad botones de la tienda.
- Cheat Codes (aunque sí implementé una fucnión para restaurar salud)
- Funcionalidad del sistema de puntos.
- Personalidad Pro y Raguequitter (todos se comportan según personalidad noob)

# Carpetas de la entrega
En la carpeta T05 se encuentran los archivos .py correspondientes al código y dentro de la carpeta res, se encuentran las imágenes (imgs) y los archivos de audio (music). Esto me recuerda, SUBE EL VOLÚMEN, HAY MÚSICA c:

Nota extra_1: El archivo Enemy .py fue utilizado para testear las distintas funcionalidades y comportamientos, sin embargo, no tiene incidencia en la entrega final. Lo dejé por temor a que si lo saco, algo pueda generar error (aunque no creo). Lo mismo se aplica para BuildBrownTowerIcon .py (no me percate de este hasta hacer el readme)

Nota extra_2: Si se juega en un notebook, puede que este no deje mover el mouse y apretar alguna tecla del keyboard al mismo tiempo. Se debe configurar esto o simplemente usar un mouse externo.

Nota_extra_3: Los iconos de los campeones son meramente referenciales, era eso que saqué de google o un monito de paint, obviamente, elegí la primera opción. De todas maneras estan implementados los campeones requeridos y el campeón extra.

Nota_extra_4: Sé que agregé muchos setters y getters que no son estrictamente necesarios, pero me gusta el color que toman las funciones en mi editor de texto. Además hacen que el código se vea mas confiable.


# Bar .py
Representa la barra de vida de las entidades.
Hereda de QGraphicsRectItem, ie, es un rectágulo rojo al cual se le agrego un texto.

Métodos importantes: 
- increment(amount): Aumenta la vida en amount unidades y la actualiza.
- decrement(amount): Disminuye y actualiza.

# BigMinion .py
Representa a un minion de los gordos c:
Hereda de DynamicGameObject, por lo que tendrá capacidad de atacar y moverse.
Recibe el parámetro power_up para indicar si le pusieron esteroides o no.

Timers importantes:
- damage_timer: timer para que adquiera un target y ataque
- move_timer: timer para que se mueva a su destino.
- detination_timer: timer para que adquiera un destino (el enemigo más cercano).

# Bullet .py
Representa una bala.
Se relaciona con la clase Sprite. Genera una Sprite al momento de impactar para dar una animación.

Timers:
- move_timer = Para moverse en linea recta según su rotación.

# Button .py
Representan botones customizables para agregar a mi GUI. Poseen señales que se activan al clickear.

__MenuButton__:
Hereda de QGraphicsRectItem, ie, es un rectángulo mas bonito nomás.
Le defini un hoverEvent de entrada y salida que hacen que cambie de opacidad.
Diseñados para ser presentado en los menú.

Metodos importantes:
- lock: Bloquea el botón para que no sea clickeable. Cambia opacidad (lo hace negro)
- unlock: Desbloquea. Restores opacity.

__GameButton__:
Hereda de MenuButton
Lo mismo que un MenuButton pero su opacidad inicial es mucho menor. Esto para que no interrumpa la experiencia de juego.

__ChampionButton__:
Hereda de QGraphicsPixmapItem, ie, es solo una imagen clickeable.
Emite señal al ser clickeado (para desbloquear el 'lock in' button)

# ChampionSignal:
Solo representa la señal que emiten los campeones al morir.

# ComputerChampion:
Se definen los campeones que son controlados por la IA.

__ComputerChampion__:
Hereda de DynamicGAmeObject.
Representa a un campeón Ia genérico.

Inicializa las variables para manejar la ulti y las señales.

Timers importantes:
sprite_timer = Para cambiar las frames.
ulti_cooldown_timer = Para controlar cuando la ulti esta available or not.
execute_ulti_timer = Para ejecutar la ulti when available (perdón el spanglish)

__ComputerMage__:
La Chau la hechicera.
Su ulti detiene los timers de ataque y moviemiento de los enemigos. Los descongela a los 5 segundos.

__ComputerTroll__:
El Hernán el magnánimo o algo así.
Mueve ferozmente a los enemigos de su lugar (los mueve de forma paralela a la recta que une al enemigo y al Hernán). Además quita bastante daño a las estructuras.

__ComputerOgrillion__:
El otro champion que habia que crear.
Su ulti tira 5 balas del armagedon cuántico. Tiene poco cooldown asi que está un poco OP.

# Delay .py
No fue usado, estaba pensado para la pausa.

# DynamicGameObject:
Se recomienda leer primero StaticGameObject.
Modela entidades que se mueven y atacan.

Métodos importantes:
- set_range(Scale_factor): Da como atributo un QgraphicsPolygonItem que será el indicado de demarcar su rango. (ESTOS POLÍGONOS LOS DEJÉ LIGERAMENTE VISIBLES PARA QUE SE OBSERVE MEJOR EL RANGO, EN UNA VERSIÓN FINAL DEBEN ESTAR INVISIBLES)
- fire: Dispara.
- acquire_target: Hace que el enemigo más cercano sea su target.
- should_be_moving: Si esta cerca de objetivo, it should not be moving.
- move_forward: Mueve al loquito. EL método de evitar colisinoes es un poco rustico, pero prefiero eso a que se queden pegados para la eternidad :C
- set_dest_to_closest: De todos los enemigos, su objetivo será la entidad más cercana.

# Game
Hereda de QGraphicsView.
Ya herman@, este es el archivo más bélico, so prepare yourself. Básicamente modelé esto como una View que muestra a una Scene. De esta forma se agregan elementos a la Scene y son mostrados por la View, que manejará señales y hará lo que tenga que hacer. Acá nace la magia de la música.

Métodos importantes: 
- start: Da comienzo al juego en sí. Initializes the player, enemy, y todos los StaticGameObject. Conecta las señales y comienza los Timers para spawnear cosas.
- spawn_player y spawn_enemy: Para revivir a los campeones cuando mueran.
- champion_died: Función que controla el evento de muerte de un campeón.
- inhibitor_died: Similar a la anterior pero para el inhibidor.
- rec_inhibitor_1 y 2: Reconstruye los inhibidores cada cierto tiempo.
- mouseMoveEvent: Para rotar al campéon en scene.
- mousePressEvent : Pra ataques normales y ultis.
- keyPressEvents: Shorcuts.
- create_allies and spawn_allies_minions: Funciones para spawnear corrctamente a los minions cada cierto tiempo. Tienen su contraparte en funciones para los minions enemigos.
- display_main_menu: Displays the main menu xdXDxdXDxDXDX
- draw_GUI: Dibuja los botones del juego en sí (ya en la partida)
- display_selection_menu: Muestra el menú para elegir campeón.
- pick_champion: Funcipon a la cual se conectan los botnoes para elegir campóein.
- pause: Pause y muestra la imagen de pause (optional). Básicamente freezea a todos los items de la scene.
- unpause: Lo contrario a pause c:
- display_pause_screen: Solo para mostrar la pantalla de pause.
- game_over: Función que controla que nexus envío la señal de muerte.
- display_game_over: Justo to show who won.
- restart: Comienza un game nuevo.
- draw_panel: Dibuja un panel para que todo sea más shoro y bonito.
- get_champion_waitin_time: generador que entrega los tiempos se´gun la formula.

# Inhibitor:
Hereda de StaticGameObject
Si muere envia señal de muerte.

# main:
It just executes the whole thing.

# Minion:
Hereda de DynamicGameObject.
Ataca a melee.

Métodos:
damage_if_colliding: Chequea si su rango colisiona con un enemigo y lo daña.

# Nexus . py:
Envia señal si muere.

# PlayerChampion:
Se modelan los campeones que serán usados por el jugador.
Se sobreescriben los keyPressEvent y keyResealeEvent para que se mueva con WASD y el mouse.

Métodos importantes:
move_to_mouse : Solo mueve al loco forward en el current angle. Choca con entidades, ie, no las traspasa.

Los demás campeones son iguales a los ya mencionados, solo que ahora heredan de PlayerChampion.

# Score:
Clase que quedó en el olvido, ya que no tuve tiempo de implementarla bien.
Va indicando cuantos puntos tiene el jugador. Solo faltó conectar con las señales adcuadas.

# Sprite:
Representa una bala al explotar.

# StaticGameObject:
La entidad base del juego. Inicializo el team, health y si es damageable o no.

# Store:
Hereda de QWidget, ie, es la ventana que se abre y representa la tienda.
Me faltó conectar sus botones para que efectivamente alteren al campeón.

# StoreIcon:
Hereda de QGRaphicsPixampItem. Es la representación en juego de la store. Solo permite ser clickeable si el campeón está muerto o e su rango.
El atributo timer se encarga de verificar si el campeón está en su rango o no.

# Tower
Representa a la torre. Hereda de StaticGameObject. Ataca al enemigo más cercano que esté dentro de su rango, similar al BIgMinion.

Fin del README C: C: C: 

 
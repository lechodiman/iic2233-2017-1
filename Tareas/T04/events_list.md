# Listado Eventos T04

- CÁTEDRA | cada 7 días | actualizar manejo de contenidos y nivel de programación.
- ACTIVIDAD | cada 7 días | fijar nivel de progreso esperado, añadir PUBLICACION NOTAS ACTIVIDAD a la lista de eventos
- AYUDANTÍA | cada 7 días | actualizar manejo de contenidos
- REUNIÓN PROFESOR | cada 7 días | actualizar nivel de programación de 10 alumnos por profesor
- CONTROL SORPRESA | Con cierta probabilidad al inicio de cada actividad | Fijar progreso de control, añadir PUBLICACIÓN NOTAS CONTROL a la lista de eventos.
- PUBLICAR TAREA | cada 14 días | define la dificultad y el nivel de progreso de la tarea. Añade RENDIR TAREA a la lista de eventos.
- RENDIR (ENTREGAR) TAREA | 14 días después de PUBLICAR TAREA | añade PUBLICACION NOTAS TAREA a la cola de tareas. Alumnos mandan mails.
- PUBLICACION [CONTROL, ACTIVIDAD, TAREA, EXAMEN] | 14 días después de [CONTROL, ACTIVIDAD, TAREA, EXAMEN] | Actualiza los niveles de confianza.
- EXÁMEN | 5 días después de última publicación de notas | define progreso del exámen. Añade PUBLICACION NOTAS EXAMEN a la lista de eventos.
- FIESTA | cada exp(1/30) días | actualiza los niveles de programación, cambia estado de alumnos que fueron a 'stunned' por dos días.
- FÚTBOL | cada exp(1/70) | cambia estado de alumnos que son afectados a 'stunned' por un día. Fija estado de la tarea siguiente a 'bélica' (+0.2)
- CORTE AGUA | cada exp(1/21) días | disminuye capacidad máxima de profesores para atender alumnos durante una semana
- ATRASO MAVRAKIS | al publicar notas con p = 0.1 | cambia el tiempo de PUBLICAR NOTAS [eval] y le suma de 2 a 5 días más
- DESCUENTO MAVRAKIS | al publicar notas con p = 0.5 | altera las notas y fija la entrega de notas como 'alterada'
- ATRASAR RENDIR TAREA | al rendir una tarea con p = 0.2 si más de 0.8 del total mandan mail | Mueve la fecha de RENDIR TAREA para dos días después. Se fija la variable tarea_atrasada = True.
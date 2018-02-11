# README T07

Archivos de la entrega:
- app.py
- github_api.py
- google_api.py
- main.py
- Procfile
- requirements.txt
- runtime.txt
- telegram_request.py

Nota importante:
Para el deploy de la aplicación a Heroky hice un *virtual enviroment* para python para que no se pusieran en requirements todas las librerias que tengo. Además, al hacer esto no tuve que hacer la definición de la variable de entorno que se menciona en el paso 6 del enunciado.

# main
Este archivo, tal como se indicaba en el enunciado, solo importa la aplicación y la corre.

# github_api
En este archivo defino las funciones relacionadas al uso de la API de GitHub, incorporé post_issue solo para probarla. Además incorporé get_comments para la aplicación del auto - comment por parte del bot.
La cuenta que realiza todos los comentarios, agregación de labels, etcétera es una cuenta creada específicamente para la tarea. Las credenciales de esta cuenta están dentro del script. Con mi cuenta personal le di acceso de colaborador al repositorio 'dummy_repo' dedicado para esta tarea.

# google_api
Acá defino funciones para identificar un bloque con código de error y para encotrar una posible solución utilizando la API de Google y el motor de búsqueda de StackOverflow.

# telegram_request
Es archivo no es relevante para la versión final. Lo usé solo para probar cómo funcionaba la API de Telegram. Lo dejé porque le tengo cariño <3

# app
Es el archivo principal para la aplicación.
En las primeras líneas se encuentra el token del bot y la url para acceder a la API.

Acá tambien implemento las funciones para interactuar con la API de Telegram.
Para almacenar una lista de contactos, implemente el CHAT_ID_SET, que corresponde a un set de python que almancena los chat id de los usuario que activaron el comando /add. Notar que si el servidor de Heroku se apaga, esta lista se vaciará.

Dentro de la aplicación en sí, defino dos rutas:
- '/': Ruta que recibe los updates de Telegram. Hice Webhook del bot de Telegram y le asigné esta ruta. 
- '/github_handler':  Ruta que recibe los update de Github. Hice webhook del repositorio 'dummy_repo' para que informe de los Issue Event. Enviará mensajes a todos los que tenga agregados en el ChAT_ID_SET. También se incorporó el Bonus, es decir, si se crea una issue con un error de python, el bot comentará automáticamente. Además, si la issue se cierra solo con el comentario automáticol bot o con ese comentario y comentarios del autor, el bot agregará la issue 'Googleable'.

Los comandos soportados por el bot son:
- send_test: Envia 'test' y el chat id de la persona que le habló.
- send_hi: Saluda. (Estos dos comandos fueron implementados para aprender de la API de Telegram)
- get: Implementada según el enunciado
- post: Ídem
- label: Ídem
- close: Ídem 
- add: Te añade al set que almacena los id. De esta forma recibirás las actualizaciones recibidas por 'github_handler'.
- remove: Te quita del set. Así no te hará spam.


Fin del REAMDE c:


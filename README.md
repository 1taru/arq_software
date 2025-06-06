# 06/junio
Añadi mas servicios pero no los he testeado lo suficiente, ojo que puse todos los puertos en 5050, asi que hay que abrir el docker mediante: 
docker run -d -p 5050:5000 jrgiadach/soabus:v1
# Explicaciones

El proyecto esta organizado por un cliente, que es el que simula la toma de una accion en este proyecto, en donde dice que es lo que quiere hacer "ejemplo: tomar una hora con el rut 12345678-9 el 2024-10-02 a las 13:50", en donde luego se es enviado al bus (que corre en el docker que subio el profe) y luego debe ser direccionado hacia el servicio correspondiente que esta dentro de la carpeta servicios

Ademas esta la carpeta ejemplo_profe que es el servicio y cliente de la aplicacion de calculadora, que es bien simple pero se supone que eso ya deberia estar funcionando con el bus que nos subio el profe

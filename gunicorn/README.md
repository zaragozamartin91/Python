Ejemplo de python + flask + Docker
----------------------------------

Para correr el ejemplo:
* Abrir una terminal de docker
* Situarse sobre el directorio del ejemplo
* Correr "docker build -t gunicornex ."
* Correr "docker run -p 5000:8000 -v "$PWD":/usr/src/app gunicornex"
* Abrir browser en http://192.168.99.100:5000/ (reemplazar la ip por aquella de tu docker host. No se accede mediante LOCALHOST!)


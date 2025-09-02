<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Componente de Mensajería</h3>

  <p align="center">
    Componente que permite el envío de eventos basados en la guía TEI a un servidor configurable 
    <br />
    <a href="https://interoperabilidad.minsal.cl/fhir/ig/tei/0.2.1/index.html"><strong>Guía TEI »</strong></a>
    <br />
    <br />
    <a href="https://github.com/cens-chile/mensajeria-productor-tei">Repositorio</a>
    &middot;
    <a href="https://github.com/cens-chile/mensajeria-productor-tei/issues/new?labels=bug&template=bug-report---.md">Reportar Bug</a>
    &middot;
    <a href="https://github.com/cens-chile/mensajeria-productor-tei/issues/new?labels=enhancement&template=feature-request---.md">Solicitar Funcionalidades</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#acerca-del-proyecto">Acerca del Proyecto</a>
      <ul>
        <li><a href="#construido-con">Desarrollado con</a></li>
      </ul>
    </li>
    <li>
      <a href="#como-empezar">Como Empezar</a>
      <ul>
        <li><a href="#requisitos-del-sistema-operativo">Requisitos del sistema operativo</a></li>
        <li><a href="#hardware-recomendado">Hardware recomendado</a></li>
        <li><a href="#prerrequisitos">Prerequisitos</a></li>
        <li><a href="#instalación">Instalación</a></li>
        <li><a href="#desarrollo">Desarrollo</a></li>
      </ul>
    </li>
    <li>
      <a href="#uso">Uso</a>
      <ul>
        <li><a href="#funcionalidades">Funcionalidades</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contribuir">Contribuir</a></li>
    <li><a href="#licencia">Licencia</a></li>
    <li><a href="#contacto">Contacto</a></li>
    <li><a href="#agradecimientos">Agradecimientos</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## Acerca del Proyecto

El sistema de salud en Chile se estructura en niveles (primario, secundario y terciario), 
siendo el nivel primario el con mayor despliegue en el territorio, con atenciones de menor complejidad
y la puerta de entrada a todas las atenciones de salud en la red pública de establecimientos. 
Para optar a una atención de especialidad, las personas deben ser derivadas desde la atención primaria 
a un centro de mayor complejidad, teniendo que esperar para recibir esta atención en el nivel secundario o terciario.

Las personas y tiempos que deben esperar para una atención de salud han sido y son una preocupación para todo el 
sistema sanitario.

Los sistemas que soportan actualmente la información de las personas y tiempos de espera por su estructura y forma
de operar, no permiten conocer la realidad de la situación, trazar al paciente y tampoco permite mantener informado
al paciente. Para mejorar la gestión de la red asistencial y la coordinación entre sus niveles, se requiere implementar
un proceso interoperable de solicitud de nueva consulta de especialidad desde APS a nivel secundario, para patologías
no adscritas a las garantías explícitas de salud (GES).

El componente de Mensajería en particular permite ejecutar el proceso de envío de los eventos, por medio de una API de envío y
consulta de estado de mensajes, los cuales pueden ser integrados con algun visor o consumidos directo desde algun servicio.
Cuenta con un proceso simple de gestión de errores y reintento de mensajes.

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



### Construido con

* [![Python][Python.org]][Python-url]
* [![Django DRF][DjangoREST.org]][DjangoREST.org]
* [![Postgres][Postgres.org]][Postgres-url]
* [![RabbitMQ][RabbitMQ.com]][RabbitMQ-url]
* [![Celery][Celery.org]][Celery-url]
* [![Git][Git-scm.com]][Git-url]
* [![Docker][Docker.com]][Docker-url]


<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- GETTING STARTED -->
## Como Empezar

Inicialmente se necesita un servidor donde desplegar el componente de mensajería con acceso a internet

### Requisitos del sistema operativo

* GNU/Linux 3.10 o superior.

### Hardware recomendado

* 4 GB
* 20 GB o más de espacio de disco duro.

### Prerrequisitos

* [Instalación de Docker](https://docs.docker.com/desktop/setup/install/linux/)
* [Instalación de GIT](https://git-scm.com/downloads/linux)


### Instalación

1. Clone the repo
    ```sh
    cd $HOME/
    git https://github.com/cens-chile/mensajeria-productor-tei
    ```
2. Generar llave para JWT
    ```bash
    cd /root/
    openssl genrsa -out $HOME/private-mensajeria.pem 2048
    openssl rsa -in $HOME/private-mensajeria.pem -outform PEM -pubout -out $HOME/public-mensajeria.pem
    ```
3. Ingresar al directorio
    ```bash
    cd /etc/profile.d/
    ```
4. Crear archivo para para almacenar las llaves generadas
    ```sh
    nano mensajeria-keys.sh
    ```
5. Ingresamos lo siguiente en el archivo y luego guardamos
    ```bash
    export PUBLIC_KEY=$(cat $HOME/public-mensajeria.pem)
    export PRIVATE_KEY=$(cat $HOME/private-mensajeria.pem)
    ```
6. Cargar variables de ambiente
    ```sh
    source /etc/profile.d/mensajeria-keys.sh
    ```   
7. Ingresamos al directorio en donde se descargo el código
    ```sh
    cd $HOME/mensajeria-productor-tei
    ```  
8. Creamos el arhivo con las variables de ambiente
    ```sh
    nano .env
    ```  
9. Ingresamos las variables de ambiente al archivo **.env**
    ```env
    DEBUG=True
    DATABASE_NAME=mensajeria
    DATABASE_HOST=master-db
    DATABASE_USER=postgres
    DATABASE_PASSWORD=mensajeria
    DATABASE_PORT=5432
    SECRET_KEY='$*=2!0l51=t_h-+mib3k!02f3h4ww!!^6ez3iov1=8w@meu0n2'
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_PASSWORD=admin
    GUNICORN_LOG_LEVEL=debug
    TEI_FHIR_SERVER=https://apicloudqa.minsal.cl/fhir/$$process-message
    TEI_AUTH_SERVER=https://apicloudqa.minsal.cl/oauth/token
    TOKEN_USER=user
    TOKEN_PASSWORD=pass
    RABBITMQ_HOST=rabbitmq
    MEMCACHED_SERVER=memcached
    ```
| Variable                  | Descripción                                                                                                     | Ejemplo                                              |
|:------------------------- |:---------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------|
| DEBUG                     | Valor para detallar si se desplegaran mensajes del modo DEBUG(true, false)                                      | DEBUG=True                                           |
| DATABASE_NAME             | Nombre de la base de datos(modificar en caso de externalizar la base de datos)                                  | midb                                                 |
| DATABASE_HOST             | Host de la base de datos(modificar en caso de externalizar la base de datos)                                    | master-db                                            |
| DATABASE_USER             | Usuario de la base de datos                                                                                     | admin                                                |
| DATABASE_PASSWORD         | Password de la base de datos                                                                                    | admin                                                |
| DATABASE_PORT             | Puerto de la base de datos(modificar en caso de externalizar la base de datos)                                  | 5432                                                 |
| SECRET_KEY                | Conjunto de caracteres para firma criptográfica use [djecrety.ir](https://djecrety.ir/) para geenrar un valor   | '$*=2!0l51=t_h-+mib3k!02f3h4ww!!^6ez3iov1=8w@meu0n2' |
| DJANGO_SUPERUSER_USERNAME | Nombre de super usuario de la API                                                                               | admin                                                |
| DJANGO_SUPERUSER_PASSWORD | Password de super usuario de la API                                                                             | admin                                                |
| GUNICORN_LOG_LEVEL        | Detalla la granuralidad de los errores('debug', 'info', 'warning', 'error','critical')                          | info                                                 |
| TEI_FHIR_SERVER           | Enpoint FHIR del servidor de destino de los mensajes(ruta del $process-message)                                 | https://apicloudqa.minsal.cl/fhir/$$process-message  |
| TEI_AUTH_SERVER           | Endpoint del servidor de autenticación para el servidor FHIR                                                    | https://apicloudqa.minsal.cl/oauth/token             |
| TOKEN_USER                | Token De usuario asignado por MINSAL                                                                            | misuario                                             |
| TOKEN_PASSWORD            | Password de Usuario asignado por MINSAL                                                                         | mipassword                                           |
| RABBITMQ_HOST             | Host del servidor broker de mensajes(modificar en caso de externalizar el servidor RabbitMQ)                    | rabbitmq                                             |
| MEMCACHED_SERVER          | Host del servidor de memcached(modificar en caso de externalizar el servidor RabbitMQ)                          | memcached                                            |
    
* Puesta en marcha(solo la API)
    ```bash
    docker compose up -d
    ```
* Puesta en marcha(API + Visor)

  ```bash
  git clone https://github.com/cens-chile/visor-tei
  echo -e \
  "{
    \"api_url\": \"http://localhost:8002/\", 
    \"defaultLimit\": 200,
    \"defaultOffset\": 0
  }" | tee visor-tei/src/config/config.json
  docker compose up -d
  ``` 

* API: Esta quedará ejecutándose en http://localhost:8002/
* Visor: Esta quedará ejecutándose en http://localhost:3000/

### Desarrollo

* Iniciar los servicios

```bash
docker compose up -d 
```

* Recompilar cambios y reiniciar servicios

```bash
docker compose up -d --build
```

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>

<!-- USAGE EXAMPLES -->
## Uso

* Accedemos a http://\<IP\>:8002 para ver las opciones que nos entrega la Documentación de la API en la especificación de OpenAPI

### Funcionalidades

* **_/api/check/_**: Valida el token generado
* **_/api/logout/_**: Permite invalidar el token de refresco para no renovar token
* **_/api/message/_**: Permite obtener la lista de mensajes enviados
* **_/api/message/<id_mensaje>_**:  Permite obtener un mensaje en particular
* **_/api/message/$process-message_**: Permite enviar el Bundle de un evento
* **_/api/token/_**: Permite generar un nuevo token con las credenciales
* **_/api/token/refresh/_**: Permite generar un nuevo token a partir del refresh token
* **_/api/token/_**: Permite generar un nuevo token con las credenciales
* **_/groups/_**: Permite adminstrar grupos
* **_/users/_**: Permite adminstrar usuarios


### Manipulación de Usuarios

* Por defecto el usuario admin por defecto tiene las funcionalidades de enviar y manipular mensajes, 
en caso de requerir otras opciones, es posible crear usuarios adicionales con otros privilegios.
* Es necesario usar credenciales del usuario administrador.
* Puede usar http://\<IP\>:8002/api/schema/swagger-ui

```curl
curl -X 'POST' \
  'http://<IP>:8002/api/token/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "admin",
  "password": "admin"
}'
```

#### Crear Grupo "sender"

* Este grupo permite asociar a usuarios que se desea que pueda enviar mensajes pero sin manipulación de usuarios.

  * Crear Grupo

```curl
curl -X 'POST' \
  'http://<IP>:8002/groups/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "sender"
}'
```

#### Crear Usuario y Asociar Grupo

* Crear un usuario y asignar el grupo creado en el paso anterior usando su ID
  * **is_active**: si el usuario está activo
  * **is_staff**: si el usuario puede manipular usuarios grupos y mensajes
  * **groups**: agregue el grupo("http://\<IP\>:8002/groups/\<ID\>/") si desea que el usuario pueda manipular mensajes
  
```curl
curl -X 'POST' \
  'http://<IP>:8002/users/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "test",
  "email": "user@example.com",
  "groups": [
     "http://localhost:8002/groups/10/"
  ],
  "password": "test",
  "is_active": true,
  "is_staff": false
}'
```

* Use las credenciales del usuario creado para obtener un nuevo token

```curl
curl -X 'POST' \
  'http://<IP>:8002/api/token/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "test",
  "password": "test"
}'
```

* Use el token obtenido en el paso anterior y úselo para el envio de mensajes.
  * **Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...**

```curl
curl -X 'POST' \
  'http://<IP>:8002/api/message/$process-message' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...' \
  -H 'Content-Type: application/json' \
  -d '{
  "resourceType": "Bundle"
  ...
}'
```

Para ejemplos de los Bundle de eventos consultar la [Documentación](https://interoperabilidad.minsal.cl/fhir/ig/tei/0.2.1/index.html)

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>




<!-- ROADMAP -->
## Roadmap

- [x] Envío de Mensajes
- [x] Reintento de Mensajes
- [ ] Nuevas Funcionalidades
    - [ ] Otro
    - [ ] Otro

Ver la sección de [open issues](https://github.com/cens-chile/mensajeria-productor-tei/issues) para una lista complete de las nuevas funcionalidades (y errores conocidos).

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- Contribuir -->
## Contribuir

Toda contribución que hagas será agradecida

Si tienes alguna sugenrencia para hacer mejor este proyecto, por favor crea tu fork y crea un pull request. También puedes abrir un issue con el tag "mejora"
No olvides dar una estrella al proyecto! Gracias!

1. Crea un fork de este proyecto
2. Crea un branch para tu funcionalidad (`git checkout -b feature/AmazingFeature`)
3. Haz el Commit con tus cambios(`git commit -m 'Add: mi funcionalidad'`)
4. Sube tus cambios al repositorio (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Top contributors:

<a href="https://github.com/cens-chile/mensajeria-productor-tei/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=cens-chile/mensajeria-productor-tei" />
</a>

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- LICENSE -->
## Licencia

Apache 2.0

Ver el archivo incluido `LICENSE` para detalles.

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- CONTACT -->
## Contacto

Interoperabilidad - [@CENSChile](https://x.com/CENSChile) - interoperabilidad@cens.cl

Link al Proyecto: [https://github.com/cens-chile/mensajeria-productor-tei](https://github.com/cens-chile/mensajeria-productor-tei)

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Agradecimientos

* Equipo CENS

<p align="right">(<a href="#readme-top">volver al inicio</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/cens-chile/mensajeria-productor-tei.svg?style=for-the-badge
[contributors-url]: https://github.com/cens-chile/mensajeria-productor-tei/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/cens-chile/mensajeria-productor-tei.svg?style=for-the-badge
[forks-url]: https://github.com/cens-chile/mensajeria-productor-tei/network/members
[stars-shield]: https://img.shields.io/github/stars/cens-chile/mensajeria-productor-tei.svg?style=for-the-badge
[stars-url]: https://github.com/cens-chile/mensajeria-productor-tei/stargazers
[issues-shield]: https://img.shields.io/github/issues/cens-chile/mensajeria-productor-tei.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/badge/Apache-LICENSE-as?style=for-the-badge&logo=apache
[license-url]: https://github.com/cens-chile/mensajeria-productor-tei/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/cens-chile-red?style=for-the-badge&labelColor=blue
[linkedin-url]: https://linkedin.com/in/othneildrew
[Python-url]: https://www.python.org/
[Python.org]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Postgres.org]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[RabbitMQ.com]: https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white
[RabbitMQ-url]: https://www.rabbitmq.com/
[DjangoREST-url]: https://www.django-rest-framework.org/
[DjangoREST.org]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[Celery.org]: https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4
[Celery-url]: https://docs.celeryq.dev/en/stable/getting-started/introduction.html
[Git-scm.com]: https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white
[Git-url]: https://git-scm.com/
[Docker.com]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/

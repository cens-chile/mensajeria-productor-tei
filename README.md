# mensajeria-productor-tei


## Requerimientos

* 1 gb de RAM
* Requiere Python 3.12 instalado

## Instalación

```bash
pip install -r requirements
python manage.py makemigrations
python manage.py migrate
```

## Creación superusuario

```bash
python manage.py createsuperuser --username admin --email admin@example.com
```

## Puesta en Marcha

## Generar llave para JWT

```bash
cd /root/
openssl genrsa -out $HOME/private-mensajeria.pem 2048
openssl rsa -in $HOME/private-mensajeria.pem -outform PEM -pubout -out $HOME/public-mensajeria.pem
```
### Variables de entorno

* Nos ubicamos en el siguiente directorio

```bash
cd /etc/profile.d/
```
* Creamos un archivo para almacenar nuestras keys

```bash
nano mensajeria-keys.sh
```

* Ingresamos lo siguiente en el archivo y luego guardamos

```bash
export PUBLIC_KEY=$(cat $HOME/public-mensajeria.pem)
export PRIVATE_KEY=$(cat $HOME/private-mensajeria.pem)
```
* Cargar variables de ambiente

```bash
source /etc/profile.d/mensajeria-keys.sh
```

* crear .env

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

## Puesta en marcha

```bash
docker compose up -d
```

## Acceso

* http://0.0.0.0:8002/api/schema/swagger-ui/


# Desarrollo

## Inicio

* Iniciar los servicios

```bash
docker compose up -d 
```

## Recompilar cambios y reiniciar servicios

```bash
docker compose up -d --build
```

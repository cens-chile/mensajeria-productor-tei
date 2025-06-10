# mensajeria-productor-tei

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

```bash
python manage.py runserver
```

## Acceso

* http://127.0.0.1:8000/api/schema/swagger-ui/
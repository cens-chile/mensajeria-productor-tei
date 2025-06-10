from django.db import models
# Create your models here.


ESTADOS = (
    ('Enviado', 'enviado'),
    ('En Proceso', 'en_proceso'),
    ('Reintento', 'reintento'),
    ('Error', 'error')
)

EVENTOS = (
    ('Inciar', 'iniciar'),
    ('Referenciar', 'referenciar'),
    ('Revisar', 'revisar'),
    ('Priorizar', 'priorizar'),
    ('Agendar', 'agendar'),
    ('Atender', 'atender'),
    ('Terminar', 'terminar')
)

class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    id_interconsulta = models.IntegerField()  # Foreign key to another model (interconsulta)
    evento = models.CharField(max_length=11, blank=False, default='iniciar', choices=EVENTOS)
    estado = models.CharField(max_length=10, blank=False, default='en_proceso', choices=ESTADOS)
    organizacion = models.CharField(max_length=255)
    fecha_envio = models.DateTimeField()
    intento = models.IntegerField()
    fecha_recepcion = models.DateTimeField()
    mensaje_resultado = models.TextField()

    def __str__(self):
        return f"Mensaje ID: {self.id_mensaje}"

from datetime import timezone

from django.db import models
# Create your models here.


ESTADOS = (
    ('enviado', 'Enviado'),
    ('en_proceso', 'En Proceso'),
    ('reintento', 'Reintento'),
    ('error', 'Error')
)

EVENTOS = (
    ('iniciar', 'Iniciar'),
    ('referenciar', 'Referenciar'),
    ('revisar', 'Revisar'),
    ('priorizar', 'Priorizar'),
    ('agendar', 'Agendar'),
    ('atender', 'Atender'),
    ('terminar', 'Terminar')
)

class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    id_interconsulta = models.CharField(max_length=255)
    evento = models.CharField(max_length=11, blank=False, default='iniciar', choices=EVENTOS)
    estado = models.CharField(max_length=10, blank=False, default='en_proceso', choices=ESTADOS)
    organizacion = models.CharField(max_length=255)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    intento = models.IntegerField(default=1)
    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    mensaje_resultado = models.TextField()

    def __str__(self):
        return f"Mensaje ID: {self.id_mensaje}"

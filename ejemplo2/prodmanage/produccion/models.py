from django.db import models

# Create your models here.
class cajas_producidas(models.Model):
    serial = models.CharField(max_length = 7)
    codigo = models.CharField(max_length = 2)
    especie = models.CharField(max_length = 50)
    variedad = models.CharField(max_length = 50)
    procedencia = models.CharField(max_length = 50)
    anio_produccion = models.CharField(max_length = 50)

    def __unicode__(self):
        return self.especie

    def cantidad(self):
        return u'%s' % cajas_producidas.objects.count()

    class Meta:
        verbose_name = "Cajas producidas"
        db_table = "cajas_producidas"
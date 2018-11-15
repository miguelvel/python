# -*- coding: utf-8 -*-
from django.contrib import admin
from produccion.models import cajas_producidas

class CajasProducidasAdmin(admin.ModelAdmin):
    list_display = ('especie','variedad','procedencia','anio_produccion','cantidad')
    search_fields = ('serial',)
admin.site.register(cajas_producidas, CajasProducidasAdmin)

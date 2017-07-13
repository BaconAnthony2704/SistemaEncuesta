# -*- coding: utf-8                   	from __future__ import unicode_literals

from django.contrib import admin
from .models import *
from django.forms import Textarea
from import_export.admin import ImportExportModelAdmin
# Register your models here.



class EncuestaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	list_display=('titulo','habilitado')
	list_filter=('titulo',)
	

class PreguntaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	search_fields=('nombre',)
	list_display = ('nombre','encuesta','objetar')
	list_filter=['encuesta']
	ordering=('-nombre','-encuesta',)
	fields=('nombre','encuesta')

class RespuestaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	list_display=('titulo','pregunta','frecuencia')
	search_fields=('titulo',)
	fields=('pregunta','titulo')

class RegistroIPAdmin(admin.ModelAdmin):
	list_display=('direccion','idencuesta','hora')
	#search_fields('direccion')
class ReporteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
	list_display=('descripcion','encuesta')
	fields=('encuesta','descripcion')


admin.site.register(Encuesta,EncuestaAdmin)
admin.site.register(Pregunta,PreguntaAdmin)
admin.site.register(Respuesta,RespuestaAdmin)
admin.site.register(RegistroIP,RegistroIPAdmin)
admin.site.register(Reporte,ReporteAdmin)

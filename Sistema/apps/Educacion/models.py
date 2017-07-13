# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.db.models.signals import post_delete
from django.dispatch import receiver

from django.db import models
from django.core.validators import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from apps.Educacion.models import *

# Create your models here.



#Tabla de encuesta en MySql
class Encuesta(models.Model):
	titulo=models.CharField(
    max_length=50,
    unique=True,
    validators=[
    #RegexValidator se utiliza para validar los caracteres que no son necesarios y que no se 
    #utilizan en el campo de ingresar una encuesta
        RegexValidator(
            regex='^[a-zA-Z0-9áéíóúñÑ ]*$',
            message='La encuesta no debe poseer caracteres ni numeros ',
            code='invalid_username'
        ),
    ]
	)
	habilitado=models.BooleanField(default=True)

	#metodo para obtener cuantas preguntas hay por cada encuesta
	@property
	def realizadas(self):
		mostrar=RegistroIP.objects.filter(idencuesta=self.id)
		contar_mostrar=mostrar.count()
		return '%i' %(contar_mostrar)



	class Meta:
		verbose_name='Encuesta'
		verbose_name_plural='Encuestas'
	def __str__(self):
		return '%s' %(self.titulo)

#Tabla pregunta, presenta una llave foranea de encuesta
class Pregunta(models.Model):
	nombre=models.CharField(
    max_length=200,
    unique=True,
    validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9áéíóúñÑ¿? ]*$',
            message='La pregunta debe de ser solo letras sin caracteres ',
            code='invalid_username'
        ),
    ]
	)
	encuesta=models.ForeignKey(Encuesta)
	objetar=models.BooleanField(default=False)

	class Meta:
		verbose_name='Pregunta'
		verbose_name_plural='Preguntas'
	def __unicode__(self):
		return '%s %s' %(self.nombre, self.encuesta)

#Tabla Respuesta, se tiene una llave foranea de pregunta
class Respuesta(models.Model):
	pregunta = models.ForeignKey(Pregunta)
	titulo = models.CharField(max_length=60,
    validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9áéíóúñÑ$ ]*$',
            message='La respuesta no debe contener caracteres especiales ',
            code='invalid_username'
        ),
    ]
    )
	frecuencia = models.IntegerField(default=0)
	#Funcion para obtener nombre de las respuestas
	#def nombre_encuesta(self):
	#	pregunta = Pregunta.objects.filter(encuesta_id = self.pregunta.id) #filtramos la clase relacional immediata
	#	return '%s' %(self.pregunta.encuesta)				#accedemos a  los elementos mediante los queryset
	class Meta:
		verbose_name='Respuesta'
		verbose_name_plural='Respuestas'
	def __str__(self):
		return '%s' %(self.titulo)

class RespuestaFiltro(models.Model):
	idpregunta=models.IntegerField()
	class Meta:
		verbose_name='RespuestaFiltro'
		verbose_name_plural='RespuestasFiltro'
	def __str__(self):
		return '%s' %(self.idpregunta)
#Tabla IP, se obtiene para capturar la direccion IP del encuestado
class RegistroIP(models.Model):
	direccion=models.CharField(max_length=50)
	idencuesta=models.IntegerField()
	hora=models.CharField(max_length=10)
	class Meta:
		verbose_name='RegistroIP'
		verbose_name_plural='RegistrosIP'
	def __str__(self):
		return '%s' %(self.direccion)
#Tabla para generar un resumen de todas las encuesta realizadas, posee una conclusion de cada encuesta1																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																								
class Reporte(models.Model):
	descripcion=models.TextField(max_length=200)
	encuesta=models.ForeignKey(Encuesta)

	class Meta:
		verbose_name='Reporte'
		verbose_name_plural='Reportes'
	def __unicode__(self):
		return '%s %s' %(self.descripcion, self.encuesta)

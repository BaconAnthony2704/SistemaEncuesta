from __future__ import unicode_literals
from __future__ import absolute_import
from django.conf.urls import url
from apps.Educacion.views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$',index),
	url(r'^encuesta/',encuesta,name='consultarEncuesta'),
	url(r'^tablas/',tablas,name='vertablas'),
	url(r'^reporte/', reporte),
	
	url(r'^pregunta/(?P<id_encuesta>\d+)/$',pregunta,name='consultarPregunta'),
	url(r'^preguntaDetalle/(?P<id_pregunta>[0-9]+)/$', pregunta_select, name='detalle_pregunta'),
	url(r'^(?P<pregunta_id>[0-9]+)/estadistica/$', estadistica, name='estadistica'),
	url(r'^registroIp/',registroIPa,name='registroIp'),
	url(r'^seguimiento/(?P<id_encuesta>\d+)/$',verSeguimiento,name='seguimiento'),
	url(r'^seguimientoEncuesta/',seguimientoEncuesta,name='seguimientoEnc'),
	url(r'^(?P<id_encuesta>[0-9]+)/finalizar/$', finalizar, name='finalizarA'),
	url(r'^nosotros/',nosotros),
	url(r'^graficar/(?P<pregunta_id>[0-9]+)/$',graficar,name='grafico'),
	url(r'^captchaValidar/(?P<id_encuesta>[0-9]+)/$',validar_captcha,name='validar_captcha2'),
	url(r'^seguimiento_usuario/',seguimientoEncuestaUsuario,name='ver_seguimiento_usuario'),

	



]
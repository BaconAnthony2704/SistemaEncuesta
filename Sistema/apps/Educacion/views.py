# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator,InvalidPage,EmptyPage
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import socket
import time
from django.db.models import Count,Max,Min,Sum

# Create your views here.
#Renderiza el index y la base del template index.html
def index(request):
	return render(request,'index.html', {})

def iniciar(request):
	return render(request,'iniciar.html', {})


#Renderiza la vista Nosotros donde aparace quienes realizaron el sistema de encuesta
def nosotros(request):
	return render(request,'nosotros.html', {})



#Agregar la linea de abajo para todos las vistas que necesita iniciar sesion

def encuesta(request):
	#El metodo request.META se obtiene la IP donde se esta visualizando la encuesta
	#Se va utilizar para obtener la IP y guardar para que solo pueda realizar una vez
	host=request.META.get('REMOTE_ADDR')
	#Obtenemos todas las encuesta donde sean exclusivas las encuestas activas
	encuesta=Encuesta.objects.exclude(habilitado=0)
	
	paginador=Paginator(encuesta,4)
	try:
		page=int(request.GET.get("page",'1'))
	except: 
		page=1
	try:
		encuesta=paginador.page(page)
	except(EmptyPage,InvalidPage):
		encuesta=paginador.page(paginador.num_pages)
	return render(request,'encuesta.html',{'encuestas':encuesta,'host':host})

#Vista pregunta
def pregunta(request,id_encuesta):
	#Obtenemos la Ip
	ip = request.META.get('REMOTE_ADDR')
	#Mandamos a pedir todas las encuesta que sean igual a id_encuesta, y que no hayan
	#sido respondidas
	pregunta = Pregunta.objects.filter(encuesta_id=id_encuesta, objetar=0)
	idencuesta=id_encuesta
	#Obtenemos la cantidad de preguntas que hay por encuesta
	contador=pregunta.count()
	respuesta = Respuesta.objects.filter(pregunta__encuesta__id=id_encuesta)
	bandera = RegistroIP.objects.filter(direccion=ip, idencuesta=id_encuesta).exists()
	paginador=Paginator(pregunta,4)
	try:
		page=int(request.GET.get("page",'1'))
	except: 
		page=1
	try:
		pregunta=paginador.page(page)
	except(EmptyPage,InvalidPage):
		pregunta=paginador.page(paginador.num_pages)
	return render(request,'preguntas.html',{'preguntas':pregunta, 'respuestas':respuesta,'contador':contador, 'idencuesta':idencuesta,'bandera':bandera})

#El login_required sirve para validar las paginas donde solo el administrador tiene derecho a ver
@login_required(login_url='/accounts/login/')
def tablas(request):
	encuesta=Encuesta.objects.all()
	pregunta = Pregunta.objects.all()
	respuesta = Respuesta.objects.all()
	return render(request,'tablas.html',{'encuestas':encuesta,'preguntas':pregunta,'respuestas':respuesta})

@login_required(login_url='/accounts/login/')
def reporte(request):
	#Obtenemos todas las respuestas, reporte, pregunta, encuesta y su 
	#respectivo conteo de encuesta por pregunta
	respuesta=Respuesta.objects.all()
	des_reporte=Reporte.objects.all()
	pregunta=Pregunta.objects.all()
	encuesta=Encuesta.objects.all()
	contar=Pregunta.objects.all().values('encuesta_id').annotate(total=Count("encuesta_id"))
	return render(request,'reporte.html', {'respuestas':respuesta,'des_reporte':des_reporte,'preguntas':pregunta,'encuesta':encuesta,'contar':contar})

def login(request):
    try:
        m = Member.objects.get(username__exact=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['member_id'] = m.id
            return HttpResponse("You're logged in.")
    except Member.DoesNotExist:
        return HttpResponse("Your username and password didn't match.")

        def nueva1(request):
        	encuesta=Encuesta.objects.all()
        	pregunta=Preguntas.objects.all()
	return render(request,'tablas.html',{'preguntas':pregunta, 'encuestas':encuesta})


def pregunta_select(request, id_pregunta):
	#Obtenemos las preguntas donde la llave sea igual a la llave primaria de pregunta
    pregunta = get_object_or_404(Pregunta, pk=id_pregunta)
    return render(request, 'pregunta_detalle.html', {'pregunta': pregunta})

def estadistica(request, pregunta_id):
	#Obtenemos las preguntas donde la llave sea igual a la llave primaria de pregunta
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    try:
    	#Si el metodo es POST donde la pregunta sea igual a la llave primaria de Prengunta
    	#Se obtiene las respuesta de esa pregunta
        respuesta_seleccionada = pregunta.respuesta_set.get(pk=request.POST['respuesta'])
    except (KeyError, Respuesta.DoesNotExist):
        # Redisplay the pregunta voting form.
        return render(request, 'pregunta_detalle.html', {
            'pregunta': pregunta,
            'error_message': "Debe de seleccionar una respuesta.",
        })
    else:
    	#Obtenemos la frecuencia de esa respuesta que selecciono y se va incrementando
    	#Y es asi para cada respuesta que se selecione
        respuesta_seleccionada.frecuencia += 1
        #guardamos la respuesta selecionada
        respuesta_seleccionada.save()
        #cambiamos la respuesta a (Respondida - Objetar)
        pregunta.objetar=1
        pregunta.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('educacion:consultarPregunta',args=(pregunta.encuesta_id,)))

@login_required(login_url='/accounts/login/')
#Podemos visualizar la IP donde el usuario esta haciendo la encuesta
#Solo la puede el administrador
def registroIPa(request):
	ip = request.META.get('REMOTE_ADDR')
	#print(ip[2][0])
	#prueba= RegistroIP()
	#prueba.direccion=ip2
	#prueba.save()
	return render (request,'Registro_IP.html',{'ip':ip})

#Vista donde se renderiza todas las encuesta con su muestra, encuesta realizada y faltantes
def verSeguimiento(request, id_encuesta):
	encuesta=Encuesta.objects.get(id=id_encuesta)
	pregunta = Pregunta.objects.filter(encuesta_id=id_encuesta)
	cpregunta=pregunta.count()+60
	print(cpregunta)
	return render(request,'ver_seguimiento.html',{'encuestas':encuesta,'cpregunta':cpregunta})

@login_required(login_url='/accounts/login/')
def seguimientoEncuesta(request):
	encuesta=Encuesta.objects.all()
	return render(request,'seguimientoEncuesta.html',{'encuestas':encuesta})


#Vista donde se hace la finalizacion de la encuesta
def finalizar(request,id_encuesta):

	idRegistro=id_encuesta
	ip = request.META.get('REMOTE_ADDR')
	#Obtenemos la direccion, ya anteriormente guardada
	nuevo=RegistroIP()
	nuevo.direccion=ip
	#Guardamos la hora donde se obtuvo la IP
	nuevo.hora=time.strftime("%X")
	nuevo.idencuesta=idRegistro
	nuevo.save()
	#Tomamos como la muestra estatica de 3
	#Se va utilizar la formula para obtener la muestra dada la poblacion
	muestra= 3
	encuesta=Encuesta.objects.get(id=id_encuesta)
	#Actualizamos la tabla pregunta, donde el campo objetar se hace 0
	#para que vuelva a acceder a las preguntas
	pregunta=Pregunta.objects.filter(encuesta_id=id_encuesta).update(objetar=0)
	var=RegistroIP.objects.filter(idencuesta=id_encuesta)
	var2=var.count()
	#comparamos con la muestra, para que la encuesta se cierra cuando 
	#se ha alcanzado el limite propuesto
	if var2 == muestra:
		encuesta.habilitado=0
		encuesta.save()
	return render(request,'base.html', {})



#Vista graficar, donde obtenemos los datos estadisticos de la encuesta
def graficar(request,pregunta_id):
	#Obtenemos la pregunta  que sea igual con pregunta_id
	pregunta=Pregunta.objects.get(id=pregunta_id)
	#Obtenemos la encuesta  que sea igual con encuesta_id
	encuesta=Encuesta.objects.get(id=pregunta.encuesta_id)
	#Obtenemos el maximo valor de la respuesta mas objetada
	maximo=Respuesta.objects.filter(pregunta_id=pregunta_id).aggregate(Max('frecuencia'))['frecuencia__max']
	#Obtenemos el minimo valor de la respuesta menos objetada
	minimo=Respuesta.objects.filter(pregunta_id=pregunta_id).aggregate(Min('frecuencia'))['frecuencia__min']
	#Obtenemos la suma de todas las respuesta objetadas
	suma=Respuesta.objects.filter(pregunta_id=pregunta_id).aggregate(Sum('frecuencia'))['frecuencia__sum']
	return render(request,'mostrar_grafico.html',{'pregunta':pregunta,'encuesta':encuesta, 'maximo':maximo, 'minimo': minimo,'suma':suma})

def validar_captcha(request,id_encuesta):

	id1=id_encuesta
	#Utilizamos el captcha - form que programamos en form.py
	form=CaptchaTestForm()
	if request.POST:
		#tomamos como requesito el metodo post para verificar si hizo el captcha
		form=CaptchaTestForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect(reverse('educacion:consultarPregunta',args=(id1,)))
	return render(request,'prueba/captcha.html',{'form':form,'id1':id1})

def seguimientoEncuestaUsuario(request):
	#vista que ve el usuario acerca del seguimiento
	encuesta=Encuesta.objects.all()
	return render(request,'ver_seguimiento_usuario.html',{'encuestas':encuesta})

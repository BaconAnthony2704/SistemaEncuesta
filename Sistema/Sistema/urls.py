from django.conf.urls import url,include
from django.contrib import admin
from apps.Educacion import views 
from django.contrib.auth.views import login, logout_then_login


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.Educacion.urls', namespace="educacion")),
    url(r'^$',views.index,name='index'),
    #url(r'^completar/',views.completar,name='completar'),

    url(r'^accounts/login/', login, {'template_name':'iniciar.html'}, name='iniciar'),
    url(r'^logout/', logout_then_login, name='logout'),
    url(r'^captcha/', include('captcha.urls')),
    
]


from django.contrib import admin

# Register your models here.
# Administrador. Acá se instancian las clases modelo Pregunta y Respuesta
# Aca importa las clases Pregunta y ElegirRespuesta que se necesitarán para el registro
from .models import Pregunta,ElegirRespuesta,PreguntasRespondidas, QuizUsuario

# Importo la Clase ElegirInLineFormset de Forms
#from .forms import ElegirInLineFormset

# Clase Pregunta Administrador
# Estas clases van a heredar de ElegirRespuesta los campos de texto
class ElegirRespuestaInline(admin.TabularInline):
    model = ElegirRespuesta
    can_delete = False
    max_num = ElegirRespuesta.MAXIMO_RESPUESTA
    min_num = ElegirRespuesta.MAXIMO_RESPUESTA
    #formset = ElegirInLineFormset

class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    # en inlines se crea una Tupla
    inlines = (ElegirRespuestaInline, )
    # Toma el texto y crea una lista
    list_display = ['texto',]
    # Para que la consola tenga campos de busqueda, accede a las preguntas(texto) y a una posible respuesta con __texto
    search_fields = ['texto','preguntas__texto']
    # Crea un filtro de preguntas por categorias y por nivel
    list_filter = ['categoria','nivel',]

# Clase que va mostrar los campos en pantalla
class PreguntasRespondidasAdmin(admin.ModelAdmin):
    
    list_display = ['pregunta','respuesta','correcta','puntaje_obtenido','categoria','niveles']

    class Meta:
        model = PreguntasRespondidas

# Clase que va mostrar nombre de usuario y puntaje en pantalla de admin
class UsuariosAdmin(admin.ModelAdmin):
    list_display=('usuario','puntaje_total')

admin.site.register(PreguntasRespondidas)
admin.site.register(Pregunta,PreguntaAdmin)
admin.site.register(ElegirRespuesta)
# Se agrega la nueva clase creada UsuariosAdmin
admin.site.register(QuizUsuario,UsuariosAdmin)


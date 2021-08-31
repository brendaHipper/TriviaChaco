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

# Clase que va mostrar los campos en pantalla
class PreguntasRespondidasAdmin(admin.ModelAdmin):
    
    list_display = ['pregunta','respuesta','correcta','puntaje_obtenido','categoria','niveles']

    class Meta:
        model = PreguntasRespondidas

admin.site.register(PreguntasRespondidas)
admin.site.register(Pregunta,PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuario)


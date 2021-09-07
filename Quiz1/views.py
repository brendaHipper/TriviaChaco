from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

from .forms import RegistroFormulario, UsuarioLoginFormulario

from .models import QuizUsuario, Pregunta, PreguntasRespondidas

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# método de inicio
def inicio(request):

	context = {

		'bienvenido': 'Bienvenido'

	}

	return render(request, 'inicio.html', context)

# si el usuario se logueo correctamente, se va renderizar a la pantalla de niveles
def niveles(request):

	return render(request, 'play/niveles.html')


def tablero(request):
	# tomar los primeros 10 usuarios para mostrar en el tablero de posiciones
	total_usaurios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:5]
	contador = total_usaurios_quiz.count()
	# se cre un dicc con el nombre context para pasar los valores 
	context = {

		'usuario_quiz':total_usaurios_quiz,
		'contar_user':contador
	}

	return render(request, 'play/tablero.html', context)

def reglasJuego(request):

	return render(request, 'play/reglasJuego.html')

def jugar(request):
	''' El usuario esta logueado y se ah creado automaticamente con get_or_create (devuelve una tupla) '''
	QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)
	''' Si el método de petición es POST VA entrar cuando en el formulario se valide la repuesta '''
	if request.method == 'POST':
		# Obtiene el id de la pregunta 
		pregunta_pk = request.POST.get('pregunta_pk')
		pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
		respuesta_pk = request.POST.get('respuesta_pk')

		try:
			opcion_selecionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
		except ObjectDoesNotExist:
			return redirect('resultado', pregunta_respondida.pk)

		QuizUser.validar_intento(pregunta_respondida, opcion_selecionada)

		return redirect('resultado', pregunta_respondida.pk)

	else:
		nivel = request.GET.get("nivel")
		# variable pregunta, donde accedo al método obtener_nuevas_preguntas() de la clase QuizUsuario y filtro por nivel
		pregunta = QuizUser.obtener_nuevas_preguntas(nivel)
		if pregunta is not None:
			QuizUser.crear_intentos(pregunta)

		puntajeTotal = QuizUser.puntaje_total

		context = {
			'pregunta':pregunta,
			'nivel':nivel,
			'puntajeTotal':puntajeTotal,
		}

	return render(request, 'play/jugar.html', context)


def resultado_pregunta(request, pregunta_respondida_pk):
	respondida = get_object_or_404(PreguntasRespondidas, pk=pregunta_respondida_pk)
	nivel = respondida.pregunta.nivel

	context = {
		'respondida':respondida,
		'nivel':nivel
	}
	return render(request, 'play/resultados.html', context)

def loginView(request):
	titulo = 'login'
	form = UsuarioLoginFormulario(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		usuario = authenticate(username=username, password=password)
		login(request, usuario)
		return redirect('niveles')

	context = {
		'form':form,
		'titulo':titulo
	}

	return render(request, 'Usuario/login.html', context)

def registro(request):

	titulo = 'Crear una Cuenta'
	if request.method == 'POST':
		form = RegistroFormulario(request.POST)
		# Si es formulario es válido, que guarde el mismo, y redireccione loguin
		if form.is_valid():
			form.save()
			# Una vez el registro se complete de forma correcta que redireccione a loguin
			return redirect('login')
	else:
		# de lo contrario si no es un método POST, no se le va pasar la petición POST --> request.POST
		form = RegistroFormulario()

	context = {

		'form':form,
		'titulo': titulo

	}

	return render(request, 'Usuario/registro.html', context)

# Recibe la petición de cierre de sesión. Y con la barra se redirecciona al inicio
def logout_vista(request):
	logout(request)
	return redirect('/')

#Presenta las estadisticas vistas solo para usuario admiistrador
def estadisticas(request):
    import operator
    if request.user.is_superuser:
        question = Pregunta.objects.all()
        ask_for_question = [q.my_ask() for q in question]
        acums = {
            'question_1': 0,
            'question_2': 0,
            'question_3': 0,
            'question_4': 0,
            'question_5': 0,
            'question_6': 0,
            'question_7': 0,
			'question_8': 0,
			'question_9': 0,
			'question_10': 0,

        }
        for ask in ask_for_question:
            for a in ask:
                if a['pregunta_id'] == 2 and a['correcta']:
                    acums['question_1'] = acums['question_1'] + 1
                elif a['pregunta_id'] == 3 and a['correcta']:
                    acums['question_2'] = acums['question_2'] + 1
                elif a['pregunta_id'] == 4 and a['correcta']:
                    acums['question_3'] = acums['question_3'] + 1
                elif a['pregunta_id'] == 5 and a['correcta']:
                    acums['question_4'] = acums['question_4'] + 1
                elif a['pregunta_id'] == 6 and a['correcta']:
                    acums['question_5'] = acums['question_5'] + 1
                elif a['pregunta_id'] == 7 and a['correcta']:
                    acums['question_6'] = acums['question_6'] + 1
                elif a['pregunta_id'] == 8 and a['correcta']:
                    acums['question_7'] = acums['question_7'] + 1
                elif a['pregunta_id'] == 9 and a['correcta']:
                    acums['question_8'] = acums['question_8'] + 1
                elif a['pregunta_id'] == 10 and a['correcta']:
                    acums['question_9'] = acums['question_9'] + 1

        major_question = max(acums.items(), key=operator.itemgetter(1))[0][9:]
        get_text_question = question.get(id=int(major_question)).texto
        get_level_question = question.get(id=int(major_question)).nivel
        users = User.objects.all().count()
        return render(request, 'estadisticas.html',
                      {'question': get_text_question, 'max_level': get_level_question, 'total_usr': users,
                       'user': request.user})
    else:
        return render(request, 'estadisticas.html', {'user': request.user})
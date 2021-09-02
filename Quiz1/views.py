from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import authenticate, login, logout

from .forms import RegistroFormulario, UsuarioLoginFormulario

from .models import QuizUsuario, Pregunta, PreguntasRespondidas

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
	total_usaurios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
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
			raise Http404

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
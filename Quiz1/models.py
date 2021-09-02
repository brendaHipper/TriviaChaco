from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

import random

# Se declara la Clase Pregunta que va contener las categorias y los niveles
class Pregunta(models.Model):
	CATEGORIAS = [
		('HISTORIA', 'Historia'),
		('GEOGRAFIA','Geografía'),
        ('EDUCACION', 'Educación'),
        ('ECONOMIA', 'Economía'),
		('CULTURA','Cultura'),
		('DEPORTE','Deporte')
	]

	NIVELES = [
		('FACIL', 'Facil'),
		('MEDIO', 'Medio'),
		('DIFICIL', 'Dificil')
	]

	NUMER_DE_RESPUESTAS_PERMITIDAS = 1
	# La pregunta se conectará a través de la relación con la ForeignKey de respuesta
	texto = models.TextField(verbose_name='Texto de la pregunta')
	categoria = models.CharField(max_length=50,choices= CATEGORIAS,default='')
	max_puntaje = models.DecimalField(verbose_name='Maximo Puntaje', default=3, decimal_places=2, max_digits=6)
	nivel = models.CharField(max_length=50,choices=NIVELES,default='')
	# Redefino string
	def __str__(self):
		return self.texto 

# Clase que brinda las opciones para la pregunta
class ElegirRespuesta(models.Model):
	# máximo de respuestas posibles
	MAXIMO_RESPUESTA = 4
	# esta linea lo que hace, es que cada vez que se elimine una respuesta
    # automaticamente se eliminaran las dependencias que tendran las ForeignKey
	pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
	correcta = models.BooleanField(verbose_name='¿Es esta la pregunta correcta?', default=False, null=False)
	texto = models.TextField(verbose_name='Texto de la respuesta')


	def __str__(self):
		return self.texto

# Clase usuario dode se guarda el puntaje total dl jugador
class QuizUsuario(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	puntaje_total = models.DecimalField(verbose_name='Puntaje Total', default=0, decimal_places=2, max_digits=10)

	# Método para obtener los intentos.
	def crear_intentos(self, pregunta):
		intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
		intento.save()

	# Excluir las preguntas que ya se respondieron
	def obtener_nuevas_preguntas(self,nivel):
		respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk', flat=True)
		preguntas_restantes = Pregunta.objects.filter(nivel__contains=nivel).exclude(pk__in=respondidas)
		if not preguntas_restantes.exists():
			return None
		return random.choice(preguntas_restantes)

	# Valida, si la respuesta es correcta, la guarda con puntaje, de lo contrario se guardará sin puntaje
	def validar_intento(self, pregunta_respondida, respuesta_selecionada):
		if pregunta_respondida.pregunta_id != respuesta_selecionada.pregunta_id:
			return

		pregunta_respondida.respuesta_selecionada = respuesta_selecionada
		if respuesta_selecionada.correcta is True:
			pregunta_respondida.correcta = True
			pregunta_respondida.puntaje_obtenido = respuesta_selecionada.pregunta.max_puntaje
			pregunta_respondida.respuesta = respuesta_selecionada

		else:
			pregunta_respondida.respuesta = respuesta_selecionada

		pregunta_respondida.save()

		self.actualizar_puntaje()

	def actualizar_puntaje(self):
		puntaje_actualizado = self.intentos.filter().aggregate(
			models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']

		self.puntaje_total = puntaje_actualizado
		self.save()

# Se guarda la pregunta respondida. Si la misma fue correcta por el usuario, se guardará también el puntaje obtenido
class PreguntasRespondidas(models.Model):
	quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
	pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
	respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
	correcta  = models.BooleanField(verbose_name='¿Es esta la respuesta correcta?', default=False, null=False)
	puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2, max_digits=6)
	nivel = models.CharField(default='',verbose_name='nivel',max_length=10)
# Se incorpora el formulario Django
from django import forms
from django.forms.widgets import HiddenInput

from .models import  Pregunta, ElegirRespuesta, PreguntasRespondidas
# Se importa UserCreationForm que incluye las dependencias de Django para formularios de usuario predeterminado y el formulario de creación de usuario
from django.contrib.auth.forms import UserCreationForm
# toma el usuario de nuestro modelo y el del que trae por defecto Django
from django.contrib.auth import authenticate, get_user_model

# Tomar el usuario del modelo
User = get_user_model()

class ElegirInlineFormset(forms.BaseInlineFormSet):
	def clean(self):
		super(ElegirInlineFormset, self).clean()

		respuesta_correcta = 0
		# Acá toma todos los formularios del modelo ElegirRespuesta
		for formulario in self.forms:
			# Si el formulario no es válido, hay unerror y  va retornar la misma vista
			if not formulario.is_valid():
				return
			# Si la respuesta es verdadera 	
			if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
				respuesta_correcta += 1

		try:
			# Estoy igualando al contador respuesta_correcta con la variable NUMER_DE_RESPUESTAS_PERMITIDAS de la clase Pregunta
            # Si es igual a 1 de lo contrario va arrojar una excepción (error) del tipo AssertionError
			assert respuesta_correcta == Pregunta.NUMER_DE_RESPUESTAS_PERMITIDAS
		except AssertionError:
			raise forms.ValidationError('Exactamente una sola respuesta es permitida')


class UsuarioLoginFormulario(forms.Form):
	username = forms.CharField(label='Nombre de Usuario')
	password = forms.CharField(widget=forms.PasswordInput,label='Contraseña')
	# Clean limpia los campos
	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		# Validaciones trae por defecto autenticacion
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("Este usuario No existe")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("Este Usuario No esta activo")

		return super(UsuarioLoginFormulario, self).clean(*args, **kwargs)

class RegistroFormulario(UserCreationForm):
	# campos obligatorios
    username = forms.CharField(required=True,label='Nombre de Usuario')
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True,label='Contraseña',widget = forms.PasswordInput())

    # Class meta que heredará,instanciará de usuario
    class Meta:
        model = User

        # Creamos los campos de registro
        # Voy a colocar en la lista el orden en el que quiero que aparezan los campos, y que campos renderizará
        fields = [
			'username',
			'email',
			'password1',
		]

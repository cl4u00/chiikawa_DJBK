from django import forms
import datetime # Importamos datetime para poder validar el rango de fechas
from tiendaApp.choices import tamanos
from tiendaApp.models import Categoria, Contacto, Personaje, Producto

class ProductoForm(forms.ModelForm):
    sku = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: CHK-001'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre del producto'}))
    
    # 1. Agregamos required=False para que este campo ya no sea obligatorio al guardar
    descripcion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descripción'}), 
        required=False
    )
    
    tamano = forms.ChoiceField(choices=tamanos, widget=forms.Select(attrs={'class': 'form-select'}))
    precio = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 15000'}))
    fecha_lanzamiento = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Selecciona una categoría",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    personaje = forms.ModelChoiceField(
        queryset=Personaje.objects.all(),
        empty_label="Selecciona un personaje",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Producto
        fields = '__all__'

    # --- Validaciones Personalizadas (clean) ---

    # 2. Validar que el precio sea mayor que cero (adaptado de la validación de sueldo)
    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        try:
            precio = int(precio)
        except ValueError:
            raise forms.ValidationError("El precio debe ser un número entero.")
        
        if precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero.")
        return precio

    # 3. Validar que la fecha de lanzamiento esté en un rango lógico
    def clean_fecha_lanzamiento(self):
        fecha = self.cleaned_data.get('fecha_lanzamiento')
        if fecha:
            fecha_minima = datetime.date(2020, 1, 1) # Año en que se creó Chiikawa aprox.
            fecha_maxima = datetime.date(2026, 12, 31)
            if not (fecha_minima <= fecha <= fecha_maxima):
                raise forms.ValidationError("La fecha de lanzamiento debe estar entre 2020 y 2026.")
        return fecha

    # 4. Validar que el nombre solo contenga letras y espacios
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        # Reemplazamos los espacios por nada solo para la validación de isalpha()
        if nombre and not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre debe contener solo letras y espacios.")
        return nombre

class ContactoForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'campo', 'placeholder': 'Tu nombre'}))
    correo = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'campo', 'placeholder': 'tucorreo@ejemplo.cl'}))
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'campo', 'placeholder': '¿Sobre qué quieres escribirnos?'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'campo', 'rows': 5, 'placeholder': 'Escribe tu mensaje'}))

    class Meta:
        model = Contacto
        fields = ['nombre', 'correo', 'asunto', 'mensaje']

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre and not nombre.replace(" ", "").isalpha():
            raise forms.ValidationError("El nombre debe contener solo letras y espacios.")
        return nombre

    def clean_mensaje(self):
        mensaje = self.cleaned_data.get('mensaje', '').strip()
        if len(mensaje) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return mensaje

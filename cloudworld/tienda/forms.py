from django import forms
from django.contrib.auth.models import User
from .models import Producto, Perfil
import re


class RegistroForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu email'
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
        }


    # ------------------------------------------------------------------
    # VALIDACION USERNAME
    # ------------------------------------------------------------------

    def clean_username(self):

        username = self.cleaned_data.get("username")

        if len(username) < 5:
            raise forms.ValidationError(
                "El usuario debe tener minimo 5 caracteres"
            )

        return username


    # ------------------------------------------------------------------
    # VALIDACION PASSWORD
    # ------------------------------------------------------------------

    def clean_password(self):

        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise forms.ValidationError("Minimo 8 caracteres")

        if not re.search(r"[A-Z]", password):
            raise forms.ValidationError(
                "Debe tener al menos una mayuscula"
            )

        if not re.search(r"[0-9]", password):
            raise forms.ValidationError(
                "Debe tener al menos un numero"
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise forms.ValidationError(
                "Debe tener al menos un simbolo"
            )

        return password


    # ------------------------------------------------------------------
    # VALIDACION EMAIL
    # ------------------------------------------------------------------

    def clean_email(self):

        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Este email ya esta en uso"
            )

        return email


# -----------------------------------------------------------------------------------------
# FORM PRODUCTOS
# -----------------------------------------------------------------------------------------

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = [
            "nombre",
            "descripcion",
            "precio",
            "stock",
            "categoria",
            "imagen"
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control'
            }),

            'precio': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'stock': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),

            'imagen': forms.URLInput(attrs={
                'class': 'form-control'
            }),
        }


    def clean_precio(self):

        precio = self.cleaned_data.get("precio")

        if precio < 0:
            raise forms.ValidationError(
                "El precio no puede ser negativo"
            )

        return precio


    def clean_stock(self):

        stock = self.cleaned_data.get("stock")

        if stock < 0:
            raise forms.ValidationError(
                "El stock no puede ser negativo"
            )

        return stock


# -----------------------------------------------------------------------------------------
# FORM PERFIL
# -----------------------------------------------------------------------------------------

class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ["telefono", "direccion"]

        widgets = {

            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),

            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu direccion'
            }),
        }
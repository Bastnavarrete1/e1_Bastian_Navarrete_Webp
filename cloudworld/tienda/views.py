from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import (Producto, Categoria, Perfil,Carrito, CarritoItem,Pedido, DetallePedido)
from .forms import RegistroForm, ProductoForm, PerfilForm
from .permisos import vendedor_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q

#Apis----------------------------------------------------------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductoSerializer
from .models import Categoria
from .serializers import CategoriaSerializer

import requests
#--------------------------------------------------------------------------------------------------------

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            messages.success(request, "Bienvenido nuevamente")
            return redirect("inicio")

        messages.error(request, "Credenciales incorrectas")
        return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


#--------------------------------------------------------------------------------------------------------

@login_required
def index(request):
    return render(request, "index.html", {
        "productos": Producto.objects.all(),
        "es_vendedor": request.user.groups.filter(name="Vendedor").exists()
    })


#--------------------------------------------------------------------------------------------------------

@login_required
@vendedor_required
def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente")
            return redirect("inicio")
    else:
        form = ProductoForm()

    return render(request, "crear_producto.html", {
        "form": form
    })


@login_required
@vendedor_required
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado")
            return redirect("inicio")
    else:
        form = ProductoForm(instance=producto)

    return render(request, "editar_producto.html", {
        "form": form
    })


@login_required
@vendedor_required
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        producto.delete()
        messages.success(request, "Producto eliminado")
        return redirect("inicio")

    return render(request, "confirmar_eliminar.html", {
        "producto": producto
    })


#--------------------------------------------------------------------------------------------------------

def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            grupo, _ = Group.objects.get_or_create(name="Cliente")
            user.groups.add(grupo)

            messages.success(request, "Cuenta creada correctamente")
            return redirect("login")
        else:
            messages.error(request, "Error al crear la cuenta")

    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})


#--------------------------------------------------------------------------------------------------------

@login_required
def ver_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, "perfil.html", {"perfil": perfil})


@login_required
def editar_perfil(request):
    perfil, _ = Perfil.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, instance=perfil)

        user = request.user
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_actual = request.POST.get("password_actual")

        if not username:
            messages.error(request, "El username no puede estar vacío")
            return redirect("editar_perfil")

        if not email:
            messages.error(request, "El email no puede estar vacío")
            return redirect("editar_perfil")

        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "Este email ya está en uso")
            return redirect("editar_perfil")

        if form.is_valid():
            form.save()

            user.username = username
            user.email = email

            if password:
                if not user.check_password(password_actual):
                    messages.error(request, "La contraseña actual es incorrecta")
                    return redirect("editar_perfil")
                user.set_password(password)

            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Perfil actualizado correctamente")
            return redirect("ver_perfil")

    else:
        form = PerfilForm(instance=perfil)

    return render(request, "editar_perfil.html", {
        "form": form,
        "perfil": perfil
    })


@login_required
def eliminar_perfil(request):
    if request.method == "POST":
        request.user.delete()
        messages.success(request, "Cuenta eliminada")
        return redirect("login")

    return render(request, "confirmar_eliminar_perfil.html")


#--------------------------------------------------------------------------------------------------------

@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    items = carrito.items.select_related("producto")
    total = sum(i.subtotal() for i in items)

    return render(request, "carrito.html", {
        "items": items,
        "total": total
    })


@login_required
def agregar_al_carrito(request, producto_id):
    if request.user.groups.filter(name="Vendedor").exists():
        return redirect("inicio")

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    producto = get_object_or_404(Producto, id=producto_id)

    if producto.stock <= 0:
        messages.error(request, "No hay stock disponible")
        return redirect("inicio")

    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": 1}
    )

    if not created:
        if item.cantidad >= producto.stock:
            messages.error(request, "No puedes agregar más unidades (stock máximo)")
            return redirect("ver_carrito")

        item.cantidad += 1
        item.save()

    messages.success(request, "Producto agregado al carrito")
    return redirect("ver_carrito")

#--------------------------------------------------------------------------------------------------------

@login_required
def generar_pedido(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related("producto")

    if not items.exists():
        return redirect("ver_carrito")

    total = sum(i.subtotal() for i in items)

    pedido = Pedido.objects.create(
        usuario=request.user,
        total=total
    )

    for item in items:
        producto = item.producto

        if item.cantidad > producto.stock:
            messages.error(request, f"No hay suficiente stock de {producto.nombre}")
            return redirect("ver_carrito")

        producto.stock -= item.cantidad
        producto.save()

        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item.cantidad,
            subtotal=item.subtotal()
        )

    items.delete()

    messages.success(request, "Pedido generado correctamente")
    return redirect("inicio")


@login_required
def restar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)

    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()

    return redirect("ver_carrito")


@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    item.delete()

    return redirect("ver_carrito")


#--------------------------------------------------------------------------------------------------------

@login_required
def lista_usuarios(request):
    if not request.user.is_superuser:
        return redirect("inicio")

    usuarios = User.objects.all()
    return render(request, "usuarios/lista_usuario.html", {"usuarios": usuarios})


@login_required
def editar_usuario(request, id):
    if not request.user.is_superuser:
        return redirect("inicio")

    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Este email ya está en uso")
            return redirect("editar_usuario", id=id)

        user.username = request.POST.get("username")
        user.email = email
        user.save()

        messages.success(request, "Usuario actualizado")
        return redirect("lista_usuarios")

    return render(request, "usuarios/editar_usuario.html", {"usuario": user})


@login_required
def eliminar_usuario(request, id):
    if not request.user.is_superuser:
        return redirect("inicio")

    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "Usuario eliminado")
        return redirect("lista_usuarios")

    return render(request, "usuarios/eliminar_usuario.html", {"usuario": user})

#--------------------------------------------------------------------------------------------------------

@api_view(['GET'])
def api_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_categorias(request):
    categorias = Categoria.objects.all()
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)


#--------------------------------------------------------------------------------------------------------

def api_dolar(request):
    response = requests.get("https://mindicador.cl/api/dolar")
    data = response.json()

    valor = data["serie"][0]["valor"]

    return render(request, "api_dolar.html", {
        "valor": valor
    })


#Me tuve que crear una cuenta en la pagina porque no encontre otra que me diera el clima local jaja---------------

def api_clima(request):
    url = "http://api.weatherstack.com/current?access_key=67d8ce95cf31fd44b7591e632dd64185&query=Santiago"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
    except Exception:
        return render(request, "api_clima.html", {
            "temperatura": "No disponible",
            "descripcion": "No disponible"
        })

    if "current" not in data:
        return render(request, "api_clima.html", {
            "temperatura": "No disponible",
            "descripcion": "No disponible"
        })

    temperatura = data["current"].get("temperature", "No disponible")
    descripcion = data["current"].get("weather_descriptions", ["No disponible"])[0]

    traducciones = {
                "Sunny": "Soleado",
                "Clear": "Despejado",
                "Partly cloudy": "Parcialmente nublado",
                "Cloudy": "Nublado",
                "Haze": "Bruma",
                "Rain": "Lluvia",
                "Light rain": "Lluvia ligera",
                "Heavy rain": "Lluvia intensa"
    }

    descripcion = traducciones.get(descripcion, descripcion)

    return render(request, "api_clima.html", {
        "temperatura": temperatura,
        "descripcion": descripcion
    })


#Segun lo que entendi tenia que dejarlas separadas ambas del uso individual aunque se vea feo----------------------------


def datos_externos(request):

    try:
        response_dolar = requests.get("https://mindicador.cl/api/dolar", timeout=5)
        data_dolar = response_dolar.json()
        valor_dolar = data_dolar["serie"][0]["valor"]
    except:
        valor_dolar = "No disponible"

    try:
        url_clima = "http://api.weatherstack.com/current?access_key=67d8ce95cf31fd44b7591e632dd64185&query=Santiago"
        response_clima = requests.get(url_clima, timeout=5)
        data_clima = response_clima.json()

        if "current" in data_clima:
            temperatura = data_clima["current"].get("temperature", "No disponible")
            descripcion = data_clima["current"].get("weather_descriptions", ["No disponible"])[0]

            traducciones = {
                "Sunny": "Soleado",
                "Clear": "Despejado",
                "Partly cloudy": "Parcialmente nublado",
                "Cloudy": "Nublado",
                "Haze": "Bruma",
                "Rain": "Lluvia",
                "Light rain": "Lluvia ligera",
                "Heavy rain": "Lluvia intensa"
            }

            descripcion = traducciones.get(descripcion, descripcion)
        else:
            temperatura = "No disponible"
            descripcion = "Error API"

    except:
        temperatura = "No disponible"
        descripcion = "No disponible"

    return render(request, "datos_externos.html", {
        "dolar": valor_dolar,
        "temperatura": temperatura,
        "descripcion": descripcion
    })
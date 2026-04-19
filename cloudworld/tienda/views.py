from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import (Producto, Categoria, Perfil,Carrito, CarritoItem,Pedido, DetallePedido)
from .forms import RegistroForm, ProductoForm, PerfilForm
from .permisos import vendedor_required
from django.contrib.auth import update_session_auth_hash


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
            return redirect("inicio")

        return render(request, "login.html", {"error": "Credenciales incorrectas"})

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

            return redirect("login")

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

        if not username:
            return render(request, "editar_perfil.html", {
                "form": form,
                "perfil": perfil,
                "error": "El username no puede estar vacío"
            })

        if not email:
            return render(request, "editar_perfil.html", {
                "form": form,
                "perfil": perfil,
                "error": "El email no puede estar vacío"
            })

        if form.is_valid():
            form.save()

            user.username = username
            user.email = email

            if password:
                user.set_password(password)

            user.save()

            # 🔥 mantener sesión activa
            update_session_auth_hash(request, user)

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
        return redirect("inicio")  # vendedores no compran

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    producto = get_object_or_404(Producto, id=producto_id)

    item, created = CarritoItem.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": 1}
    )

    if not created:
        item.cantidad += 1
        item.save()

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
        DetallePedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            subtotal=item.subtotal()
        )

    items.delete()

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
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()

        return redirect("lista_usuarios")

    return render(request, "usuarios/editar_usuario.html", {"usuario": user})


@login_required
def eliminar_usuario(request, id):
    if not request.user.is_superuser:
        return redirect("inicio")

    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.delete()
        return redirect("lista_usuarios")

    return render(request, "usuarios/eliminar_usuario.html", {"usuario": user})
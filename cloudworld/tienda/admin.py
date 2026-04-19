from django.contrib import admin
from .models import Producto, Categoria, Carrito, Pedido, DetallePedido, Perfil

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Carrito)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Perfil)
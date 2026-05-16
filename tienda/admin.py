from django.contrib import admin
from .models import Categoria, DetallePedido, Pedido, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'activo')
    list_filter = ('activo', 'categoria')
    search_fields = ('nombre', 'descripcion')


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal')
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'total', 'creado')
    list_filter = ('estado', 'creado')
    search_fields = ('usuario__username',)
    readonly_fields = ('usuario', 'total', 'creado')
    inlines = [DetallePedidoInline]

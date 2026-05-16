from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('productos/', views.productos_view, name='productos'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/actualizar/<int:producto_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/quitar/<int:producto_id>/', views.quitar_carrito, name='quitar_carrito'),
    path('comprar/', views.confirmar_compra, name='confirmar_compra'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('administracion/productos/', views.admin_productos, name='admin_productos'),
    path('administracion/productos/crear/', views.crear_producto, name='crear_producto'),
    path('administracion/productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('administracion/productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]

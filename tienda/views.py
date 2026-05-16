from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, ProductoForm, RegistroForm
from .models import Pedido, DetallePedido, Producto


def es_administrador(user):
    return user.is_authenticated and user.is_staff


def obtener_carrito(request):
    return request.session.setdefault('carrito', {})


def construir_items_carrito(carrito):
    productos = Producto.objects.filter(id__in=carrito.keys(), activo=True)
    productos_por_id = {str(producto.id): producto for producto in productos}
    items = []
    total = Decimal('0')

    for producto_id, cantidad in carrito.items():
        producto = productos_por_id.get(str(producto_id))
        if not producto:
            continue
        cantidad = int(cantidad)
        subtotal = producto.precio * cantidad
        total += subtotal
        items.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return items, total


def home(request):
    productos_destacados = Producto.objects.filter(activo=True, stock__gt=0)[:3]
    return render(request, 'tienda/home.html', {'productos_destacados': productos_destacados})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido/a, {user.username}!')
            return redirect('dashboard')
        messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'tienda/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistroForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, f'Cuenta creada exitosamente. ¡Bienvenido/a, {username}!')
        return redirect('dashboard')

    return render(request, 'tienda/registro.html', {'form': form})


@login_required
def dashboard_view(request):
    context = {
        'total_productos': Producto.objects.count(),
        'total_stock': sum(Producto.objects.values_list('stock', flat=True)),
        'total_pedidos': Pedido.objects.filter(usuario=request.user).count(),
        'es_admin': request.user.is_staff,
    }
    return render(request, 'tienda/dashboard.html', context)


@login_required
def productos_view(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'tienda/productos.html', {'productos': productos})


@login_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    if request.method != 'POST':
        return redirect('productos')

    cantidad = int(request.POST.get('cantidad', 1))
    if cantidad <= 0:
        messages.error(request, 'La cantidad debe ser mayor que cero.')
        return redirect('productos')

    carrito = obtener_carrito(request)
    cantidad_actual = int(carrito.get(str(producto.id), 0))
    nueva_cantidad = cantidad_actual + cantidad

    if nueva_cantidad > producto.stock:
        messages.error(request, f'Solo hay {producto.stock} unidades disponibles de {producto.nombre}.')
        return redirect('productos')

    carrito[str(producto.id)] = nueva_cantidad
    request.session.modified = True
    messages.success(request, f'{producto.nombre} agregado al carrito.')
    return redirect('carrito')


@login_required
def carrito_view(request):
    carrito = obtener_carrito(request)
    items, total = construir_items_carrito(carrito)
    return render(request, 'tienda/carrito.html', {'items': items, 'total': total})


@login_required
def actualizar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    if request.method != 'POST':
        return redirect('carrito')

    cantidad = int(request.POST.get('cantidad', 1))
    carrito = obtener_carrito(request)

    if cantidad <= 0:
        carrito.pop(str(producto.id), None)
        messages.info(request, f'{producto.nombre} fue quitado del carrito.')
    elif cantidad > producto.stock:
        messages.error(request, f'No puedes superar el stock disponible ({producto.stock}).')
    else:
        carrito[str(producto.id)] = cantidad
        messages.success(request, 'Carrito actualizado.')

    request.session.modified = True
    return redirect('carrito')


@login_required
def quitar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_carrito(request)
    carrito.pop(str(producto.id), None)
    request.session.modified = True
    messages.info(request, f'{producto.nombre} fue quitado del carrito.')
    return redirect('carrito')


@login_required
def confirmar_compra(request):
    carrito = obtener_carrito(request)
    items, total = construir_items_carrito(carrito)

    if not items:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('productos')

    if request.method != 'POST':
        return render(request, 'tienda/confirmar_compra.html', {'items': items, 'total': total})

    with transaction.atomic():
        productos_actualizados = []
        for item in items:
            producto = Producto.objects.select_for_update().get(id=item['producto'].id)
            if item['cantidad'] > producto.stock:
                messages.error(request, f'Stock insuficiente para {producto.nombre}.')
                return redirect('carrito')
            productos_actualizados.append((producto, item['cantidad']))

        pedido = Pedido.objects.create(usuario=request.user, total=total)
        for producto, cantidad in productos_actualizados:
            subtotal = producto.precio * cantidad
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal,
            )
            producto.stock -= cantidad
            producto.save(update_fields=['stock', 'actualizado'])

    request.session['carrito'] = {}
    messages.success(request, f'Compra confirmada. Pedido #{pedido.id} registrado correctamente.')
    return redirect('detalle_pedido', pedido_id=pedido.id)


@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'tienda/detalle_pedido.html', {'pedido': pedido})


@user_passes_test(es_administrador, login_url='login')
def admin_productos(request):
    productos = Producto.objects.select_related('categoria').all()
    return render(request, 'tienda/admin_productos.html', {'productos': productos})


@user_passes_test(es_administrador, login_url='login')
def crear_producto(request):
    form = ProductoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto creado correctamente.')
        return redirect('admin_productos')

    return render(request, 'tienda/producto_form.html', {'form': form, 'titulo': 'Crear producto'})


@user_passes_test(es_administrador, login_url='login')
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    form = ProductoForm(request.POST or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('admin_productos')

    return render(
        request,
        'tienda/producto_form.html',
        {'form': form, 'titulo': 'Editar producto', 'producto': producto},
    )


@user_passes_test(es_administrador, login_url='login')
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('admin_productos')

    return render(request, 'tienda/producto_confirmar_eliminacion.html', {'producto': producto})

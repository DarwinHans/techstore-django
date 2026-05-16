from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, DetallePedido, Pedido, Producto


class EcommerceFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='cliente', password='Cliente12345')
        self.admin = User.objects.create_user(
            username='admin',
            password='Admin12345',
            is_staff=True,
        )
        self.categoria, _ = Categoria.objects.get_or_create(nombre='Tecnología')
        self.producto = Producto.objects.create(
            nombre='Mouse inalámbrico',
            descripcion='Mouse ergonómico',
            categoria=self.categoria,
            precio=24990,
            stock=5,
        )

    def test_catalogo_requiere_login(self):
        response = self.client.get(reverse('productos'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_cliente_agrega_producto_y_confirma_compra(self):
        self.client.login(username='cliente', password='Cliente12345')

        response = self.client.post(
            reverse('agregar_carrito', args=[self.producto.id]),
            {'cantidad': 2},
        )
        self.assertRedirects(response, reverse('carrito'))

        response = self.client.post(reverse('confirmar_compra'))
        self.assertEqual(response.status_code, 302)

        pedido = Pedido.objects.get(usuario=self.user)
        detalle = DetallePedido.objects.get(pedido=pedido)
        self.producto.refresh_from_db()

        self.assertEqual(detalle.cantidad, 2)
        self.assertEqual(pedido.total, 49980)
        self.assertEqual(self.producto.stock, 3)

    def test_admin_crea_producto_desde_crud(self):
        self.client.login(username='admin', password='Admin12345')

        response = self.client.post(
            reverse('crear_producto'),
            {
                'nombre': 'Teclado mecánico',
                'descripcion': 'Switches azules',
                'categoria': self.categoria.id,
                'precio': 59990,
                'stock': 8,
                'activo': 'on',
            },
        )

        self.assertRedirects(response, reverse('admin_productos'))
        self.assertTrue(Producto.objects.filter(nombre='Teclado mecánico').exists())

    def test_cliente_no_accede_admin_productos(self):
        self.client.login(username='cliente', password='Cliente12345')

        response = self.client.get(reverse('admin_productos'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from tienda.models import Categoria, Producto


class Command(BaseCommand):
    help = "Crea usuarios y productos de demostración para la entrega M7/M8."

    def handle(self, *args, **options):
        admin, _ = User.objects.update_or_create(
            username="admin_demo",
            defaults={"is_staff": True, "is_superuser": True, "email": "admin@example.com"},
        )
        admin.set_password("Admin12345")
        admin.save()

        cliente, _ = User.objects.update_or_create(
            username="cliente_demo",
            defaults={"is_staff": False, "is_superuser": False, "email": "cliente@example.com"},
        )
        cliente.set_password("Cliente12345")
        cliente.save()

        tecnologia, _ = Categoria.objects.get_or_create(
            nombre="Tecnología",
            defaults={"descripcion": "Equipos y accesorios para trabajo y estudio."},
        )
        audio, _ = Categoria.objects.get_or_create(
            nombre="Audio",
            defaults={"descripcion": "Dispositivos de sonido y comunicación."},
        )

        productos = [
            ("Laptop Pro 15", "Notebook para desarrollo, estudio y productividad.", tecnologia, 899990, 12),
            ("Mouse inalámbrico", "Mouse ergonómico con conexión Bluetooth.", tecnologia, 24990, 45),
            ("Teclado mecánico", "Teclado compacto con switches mecánicos.", tecnologia, 59990, 20),
            ("Monitor 27 4K", "Monitor UHD para diseño, programación y multitarea.", tecnologia, 349990, 8),
            ("Auriculares Bluetooth", "Audífonos inalámbricos con micrófono integrado.", audio, 79990, 30),
            ("Webcam HD", "Cámara web para reuniones y clases online.", tecnologia, 44990, 15),
        ]

        for nombre, descripcion, categoria, precio, stock in productos:
            Producto.objects.update_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": descripcion,
                    "categoria": categoria,
                    "precio": precio,
                    "stock": stock,
                    "activo": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Datos demo creados: admin_demo y cliente_demo."))

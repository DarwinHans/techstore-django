from django.db import migrations


def crear_productos_iniciales(apps, schema_editor):
    Categoria = apps.get_model("tienda", "Categoria")
    Producto = apps.get_model("tienda", "Producto")

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
        Producto.objects.get_or_create(
            nombre=nombre,
            defaults={
                "descripcion": descripcion,
                "categoria": categoria,
                "precio": precio,
                "stock": stock,
                "activo": True,
            },
        )


def eliminar_productos_iniciales(apps, schema_editor):
    Producto = apps.get_model("tienda", "Producto")
    Categoria = apps.get_model("tienda", "Categoria")
    Producto.objects.filter(
        nombre__in=[
            "Laptop Pro 15",
            "Mouse inalámbrico",
            "Teclado mecánico",
            "Monitor 27 4K",
            "Auriculares Bluetooth",
            "Webcam HD",
        ]
    ).delete()
    Categoria.objects.filter(nombre__in=["Tecnología", "Audio"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0002_categoria_pedido_producto_detallepedido"),
    ]

    operations = [
        migrations.RunPython(crear_productos_iniciales, eliminar_productos_iniciales),
    ]

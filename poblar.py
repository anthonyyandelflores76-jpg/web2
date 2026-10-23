from app import app, db, Producto

productos_a_insertar = [
    # Sublimación
    {"nombre": "Gorras", "categoria": "Sublimación", "precio": 20.00},
    {"nombre": "Thermo digital", "categoria": "Sublimación", "precio": 40.00},
    {"nombre": "Reloj Sublimado", "categoria": "Sublimación", "precio": 25.00},
    
    # Merchandising
    {"nombre": "Llaveros Espejos", "categoria": "Merchandising", "precio": 2.50},
    {"nombre": "Llaveros de 44 y 56", "categoria": "Merchandising", "precio": 2.00},
    {"nombre": "Pines de 44 y 56mm", "categoria": "Merchandising", "precio": 2.00},
    {"nombre": "Imantados", "categoria": "Merchandising", "precio": 2.50},
    {"nombre": "Sticker Holográficos", "categoria": "Merchandising", "precio": 2.00},
    {"nombre": "Sticker Simples", "categoria": "Merchandising", "precio": 1.00},
    {"nombre": "Bolsa de Tela", "categoria": "Merchandising", "precio": 15.00},
    {"nombre": "Polos", "categoria": "Merchandising", "precio": 25.00},
    {"nombre": "Distintivo", "categoria": "Merchandising", "precio": 10.00},
    {"nombre": "Padmouse", "categoria": "Merchandising", "precio": 12.00},
    {"nombre": "Monederos", "categoria": "Merchandising", "precio": 8.00},
    {"nombre": "Lapiceros", "categoria": "Merchandising", "precio": 2.00},
    {"nombre": "Mochilas Escolares Bordadas", "categoria": "Merchandising", "precio": 38.00},
    {"nombre": "Globos Metalizados", "categoria": "Merchandising", "precio": 5.00},
    
    # Papelería
    {"nombre": "Afiches", "categoria": "Papelería", "precio": 2.50},
    {"nombre": "Agenditas", "categoria": "Papelería", "precio": 3.50},
    {"nombre": "Block Escolar", "categoria": "Papelería", "precio": 10.00},
    {"nombre": "Agenda holográfica", "categoria": "Papelería", "precio": 15.00},
    {"nombre": "Agenda Normal", "categoria": "Papelería", "precio": 12.00},
    {"nombre": "Agenda cartón grueso", "categoria": "Papelería", "precio": 20.00},
    {"nombre": "Folder turísticos", "categoria": "Papelería", "precio": 3.00},
    {"nombre": "Rompecabezas Educativo", "categoria": "Papelería", "precio": 10.00},
    {"nombre": "Tarjetas Caladas", "categoria": "Papelería", "precio": 10.00},
    {"nombre": "Calendario tipo pirámide", "categoria": "Papelería", "precio": 15.00},
    {"nombre": "Calendario A4", "categoria": "Papelería", "precio": 6.00},
    {"nombre": "Calendario A5", "categoria": "Papelería", "precio": 5.00},
    
    # Cristalería
    {"nombre": "Frasco grande de vidrio", "categoria": "Cristalería", "precio": 15.00},
    {"nombre": "Frasco mediano de vidrio", "categoria": "Cristalería", "precio": 10.00},
    {"nombre": "Jarra de vidrio 2 litros", "categoria": "Cristalería", "precio": 20.00},
    {"nombre": "Vaso de vidrio 1", "categoria": "Cristalería", "precio": 8.00},
    {"nombre": "Vaso de vidrio 2 delgado", "categoria": "Cristalería", "precio": 7.00},
    {"nombre": "Vaso Chop", "categoria": "Cristalería", "precio": 8.00}
]

with app.app_context():
    for item in productos_a_insertar:
        # Verificamos si ya existe para no duplicarlo
        existe = Producto.query.filter_by(nombre=item["nombre"]).first()
        if not existe:
            nuevo = Producto(
                nombre=item["nombre"],
                categoria=item["categoria"],
                precio=item["precio"],
                descripcion="Producto oficial de calidad."
            )
            db.session.add(nuevo)
    
    db.session.commit()
    print("¡Todos los productos se han agregado exitosamente a Supabase!")
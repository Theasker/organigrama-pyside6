data = {
    "empresa": "Gobierno de Aragón",
    "departamentos": {
        "Tecnología": {
            "responsable": "Mauricio Segura",
            "equipo": ["Ana", "Luis", "Marta"]
        },
        "Compras": {
            "responsable": "Elena",
            "presupuesto": 125000
        }
    },
    "inventario": {
        "portátiles": [
            {"marca": "Dell", "serie": "ABC123"},
            {"marca": "HP", "serie": "XYZ456"}
        ],
        "monitores": 42
    }
}

print(isinstance(data, dict)) # Verificar que es un diccionario
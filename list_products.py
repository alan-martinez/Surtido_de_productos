from database import establecer_conexion
from prettytable import PrettyTable

conexion = establecer_conexion()
cursor = conexion.cursor()

# Listado de todos los productos
consulta = """
    SELECT p.codigo, l.nombre, e.disponible, l.fecha_caducidad
    FROM productos p
    INNER JOIN existencias e ON p.id = e.producto_id
    INNER JOIN lotes l ON e.lote_id = l.id
    WHERE e.disponible > 0
    ORDER BY l.fecha_caducidad ASC
"""
cursor.execute(consulta)

registros = cursor.fetchall()

# Tabla con los datos relacionados
tabla = PrettyTable()
tabla.field_names = ["Código", "Lote", "Cantidad", "Fecha Caducidad"]

for registro in registros:
    tabla.add_row(registro)

print(tabla)

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()
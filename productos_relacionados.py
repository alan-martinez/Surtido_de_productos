from database import establecer_conexion
from prettytable import PrettyTable

conexion = establecer_conexion()
cursor = conexion.cursor()

codigo_producto = input("Ingrese el código del producto: ")

# Datos de los productos relacionados
consulta = """
    SELECT p.codigo AS codigo_actual, l1.nombre AS lote_actual, e1.disponible AS cantidad_actual,
           p_rel.codigo AS codigo_relacionado, l2.nombre AS lote_relacionado, e2.disponible AS cantidad_relacionada
    FROM productos p
    INNER JOIN productos_relacionados pr ON p.id = pr.product_id_i
    INNER JOIN productos p_rel ON pr.product_id_r = p_rel.id
    INNER JOIN existencias e1 ON p.id = e1.producto_id
    INNER JOIN existencias e2 ON p_rel.id = e2.producto_id
    INNER JOIN lotes l1 ON e1.lote_id = l1.id
    INNER JOIN lotes l2 ON e2.lote_id = l2.id
    WHERE p.codigo = %s AND e1.disponible > 0 AND e2.disponible > 0
    ORDER BY l1.fecha_caducidad ASC
"""
cursor.execute(consulta, (codigo_producto,))

# Obtener todos los registros de la consulta
registros = cursor.fetchall()

# Tabla con los datos relacionados
tabla = PrettyTable()
tabla.field_names = ["Código Actual", "Lote Actual", "Cantidad Actual", "Código Relacionado", "Lote Relacionado", "Cantidad Relacionada"]

for registro in registros:
    tabla.add_row(registro)

print(tabla)

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()

from database import establecer_conexion
from prettytable import PrettyTable

continuar = True  # Variable para controlar el bucle
while continuar:
    conexion = establecer_conexion()
    cursor = conexion.cursor()

    codigo_producto = input("Ingrese el código del producto: ")

    # Consulta - Busca los productos relacionados disponibles para surtir la cantidad solicitada 
    consulta_relacionados = """
        SELECT p.codigo, l1.nombre, e1.disponible,
               p_rel.codigo, l2.nombre, e2.disponible
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

    cursor.execute(consulta_relacionados, (codigo_producto,))
    registros_relacionados = cursor.fetchall()

    if registros_relacionados:
        cantidad = None
        while cantidad is None:
            try:
                cantidad = int(input("Ingrese la cantidad: "))
            except ValueError:
                print("Ingrese un número entero válido.")

        # Obtener los productos relacionados disponibles
        productos_disponibles = []
        for registro in registros_relacionados:
            codigo_relacionado = registro[3]  # -> codigo producto
            cantidad_relacionada = registro[5]  # -> cantidad relacionada
            productos_disponibles.append((codigo_relacionado, cantidad_relacionada))

        placeholders = ','.join(['%s'] * len(productos_disponibles))
        consulta_existencias = """
                SELECT p.codigo, l.nombre, e.disponible, l.fecha_caducidad
                FROM productos p
                INNER JOIN existencias e ON p.id = e.producto_id
                INNER JOIN lotes l ON e.lote_id = l.id
                WHERE p.codigo IN ({}) AND e.disponible > 0
                ORDER BY l.fecha_caducidad ASC
            """.format(placeholders)

        codigos_relacionados = [codigo for codigo, _ in productos_disponibles]
        cursor.execute(consulta_existencias, codigos_relacionados)

        registros_existencias = cursor.fetchall()

        # Continuar con el proceso de surtido utilizando los registros de existencias
        productos_surtidos = []  # Lista para almacenar los productos surtidos
        total_surtido = 0
        for codigo, lote, disponible, fecha_caducidad in registros_existencias:
            if total_surtido >= cantidad:
                break

            if (codigo, lote, disponible, fecha_caducidad) in registros_existencias:
                cantidad_surtida = min(cantidad - total_surtido, disponible)
                total_surtido += cantidad_surtida
                productos_surtidos.append((codigo, lote, cantidad_surtida))

        if productos_surtidos:
            # Crear una tabla para mostrar los datos
            tabla = PrettyTable()
            tabla.field_names = ["Código", "Lote", "Cantidad"]

            # Agregar los productos surtidos a la tabla
            for producto in productos_surtidos:
                tabla.add_row(producto)

            print(tabla)

            # Verificar si no se pudo surtir toda la cantidad solicitada
            cantidad_no_surtida = cantidad - total_surtido
            if cantidad_no_surtida > 0:
                print(f"No se pudieron surtir {cantidad_no_surtida} unidades.")
    else:
        print("No se encontraron productos relacionados.")

    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()
    
    respuesta = input("¿Desea hacer otra consulta? (Y/N): ")
    if respuesta.upper() != "Y":
        continuar = False

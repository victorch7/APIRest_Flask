#conexion a bd
from database.db import get_connection
from .entities.Product import Producto   

class ProductoModel():
    @classmethod   #Se llama sin la necesidad de llamar a la clase Producto
    def get_productos(self):
        try:
            connection = get_connection()
            productos = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre, categoria, descripcion, imagen, precio, stock FROM producto")
                resultset = cursor.fetchall()

                for row in resultset:
                    producto = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    productos.append(producto.to_JSON())

            connection.close()
            return productos
        except Exception as ex:
            raise Exception(ex)
    
    
    @classmethod   #Solo lista un producto
    def get_producto(self,id):
        try:
            connection = get_connection()
            productos = []

            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nombre, categoria, descripcion, imagen, precio, stock FROM producto WHERE id=%s",(id,))
                row = cursor.fetchone() #Selecciona uno

                producto = None
                if row != None:
                    producto = Producto(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    producto = producto.to_JSON()

            connection.close()
            return producto
        except Exception as ex:
            raise Exception(ex)
        
    #Actualizar un producto
    @classmethod
    def update_producto(self, producto):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE producto SET nombre = %s,  categoria = %s, descripcion = %s, imagen = %s, precio = %s, stock = %s  
                                WHERE id = %s""", (producto.nombre, producto.categoria, producto.descripcion, producto.imagen, producto.precio, producto.stock, producto.id))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
        
    # Método update_producto modificado en ProductoModel
    @classmethod
    def update_producto_patch(cls, producto):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("""UPDATE producto SET nombre = %s, categoria = %s, descripcion = %s, imagen = %s, precio = %s, stock = %s
                                WHERE id = %s""",
                            (producto['nombre'], producto['categoria'], producto['descripcion'], producto['imagen'], producto['precio'], producto['stock'], producto['id']))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
    
    #Agregar productos
    @classmethod
    def add_producto(self, producto):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO producto (nombre, categoria, descripcion, imagen, precio, stock) 
                                VALUES (%s, %s, %s, %s, %s, %s)""", (producto.nombre, producto.categoria, producto.descripcion, producto.imagen, producto.precio, producto.stock))
                affected_rows = cursor.rowcount #Cuantas filas se afectaron
                connection.commit()
            connection.close()
            return affected_rows #Retorna las filas afectadas
        except Exception as ex:
            raise Exception(ex)


    #Eliminar producto
    @classmethod
    def delete_producto(self, producto):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM producto WHERE id = %s", (producto.id,))
                affected_rows = cursor.rowcount
                connection.commit()

            connection.close()
            return affected_rows
        except Exception as ex:
            raise Exception(ex)
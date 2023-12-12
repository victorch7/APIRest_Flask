class Producto():
    def __init__(self, id, nombre, categoria, descripcion, imagen, precio, stock ) -> None:
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.imagen = imagen
        self.precio = precio
        self.stock = stock
        

    def to_JSON(self):  #Retorna un diccionario de los parametros para devolverlo como formato JSON
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria,
            'descripcion': self.descripcion,
            'imagen': self.imagen,
            'precio': self.precio,
            'stock': self.stock
        }
        

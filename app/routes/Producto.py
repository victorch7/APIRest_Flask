from flask import Blueprint, jsonify, request
# Entities
from models.entities.Product import Producto
# Modelos
from models.ProductModel import ProductoModel

import uuid #Genera un codigo unico a partir de la fecha y hora del momento actual

main = Blueprint('producto_bp', __name__)


@main.route('/productos',methods=['GET'])
def get_productoquery():
    try:
        id = request.args.get('id')  # Obtener el valor del query string 'id'
        if id:
            producto = ProductoModel.get_producto(id)
            if producto is not None:
                return jsonify(producto)
            else:
                return jsonify({'message': 'Se necesita proporcionar un ID válido'}), 400  # Código HTTP 400 - Solicitud incorrecta
        else:
            productos = ProductoModel.get_productos()
            return jsonify(productos)
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500  # Código HTTP 500 - Error interno del servidor
    
    
#Retorna todos los productos
@main.route('/productos')
def get_productos():
    try:
        productos = ProductoModel.get_productos()
        return jsonify(productos)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
    
#Retorna un solo producto con el id que se manda como petición
@main.route('/productos/<id>')
def get_producto(id):
    try:
        producto = ProductoModel.get_producto(id)
        if producto != None:
            return jsonify(producto)
        else:
            return jsonify({}), 404 #Codigo Http no se encontro
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500


#Insertar un producto 
@main.route('/productos/add', methods=['POST'])
def add_producto():
    try:
        nombre = request.json['nombre']
        categoria = request.json['categoria']
        descripcion = request.json['descripcion']
        imagen = request.json['imagen']
        precio = int(request.json['precio'])
        stock = int(request.json['stock'])
        # id = uuid.uuid4() #convertir a string porque es un objeto
        
        producto = Producto('', nombre, categoria, descripcion, imagen, precio, stock)
        affected_rows = ProductoModel.add_producto(producto)
        
        if affected_rows == 1: #Si afecto una fila retorna el id del nuevo producto
            return jsonify({'message': "Producto ingresado correctamente"}), 200
        else:
            return jsonify({'message': "Error al insertar"}), 500
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
    
    
#actualizar un producto
@main.route('/productos/update/<id>', methods=['PUT'])
def update_producto(id):
    try:
        nombre = request.json['nombre']
        categoria = request.json['categoria']
        descripcion = request.json['descripcion']
        imagen = request.json['imagen']
        precio = int(request.json['precio'])
        stock = int(request.json['stock'])
        
        producto = Producto(str(id), nombre, categoria, descripcion, imagen, precio, stock)

        affected_rows = ProductoModel.update_producto(producto)

        if affected_rows == 1:
            return jsonify({'message': "Producto actualizado"}), 200
        else:
            return jsonify({'message': "No se actualizo el producto"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
#actualizar un producto
@main.route('/productos/update', methods=['PUT'])
def update_productoquery():
    try:
        id = request.args.get('id')  # Obtener el valor del query string 'id'
        if id:
            nombre = request.json['nombre']
            categoria = request.json['categoria']
            descripcion = request.json['descripcion']
            imagen = request.json['imagen']
            precio = int(request.json['precio'])
            stock = int(request.json['stock'])
            
            producto = Producto(id, nombre, categoria, descripcion, imagen, precio, stock)

            affected_rows = ProductoModel.update_producto(producto)

            if affected_rows == 1:
                return jsonify({'message': "Producto actualizado"}), 200
            else:
                return jsonify({'message': "No se actualizo el producto"}), 404  
        else:
            return jsonify({}), 404  # Código HTTP 404 - No encontrado
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500

    
    
#Eliminar un produto
@main.route('/productos/delete/<id>', methods=['DELETE'])
def delete_producto(id):
    try:
        producto = Producto(id, None, None, None, None, None, None)  # Crear una instancia solo con el ID

        affected_rows = ProductoModel.delete_producto(producto)

        if affected_rows == 1:
            return jsonify({'message': f"Producto con ID {id} eliminado correctamente"})
        else:
            return jsonify({'message': "No se pudo eliminar el producto"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500



# Actualizar parcialmente un producto
@main.route('/productos/update_partial/<id>', methods=['PATCH'])
def update_producto_partial(id):
    try:
        producto_data = request.json
        producto = ProductoModel.get_producto(id)
        print(producto_data)
        print('/n')
        print(producto)
        if producto is None:
            return jsonify({'message': "Producto no encontrado"}), 404

        # Aquí actualizamos solo los campos que se proporcionan en la solicitud PATCH
        if 'nombre' in producto_data:
            producto['nombre'] = producto_data['nombre']
        if 'categoria' in producto_data:
            producto['categoria'] = producto_data['categoria']
        if 'descripcion' in producto_data:
            producto['descripcion'] = producto_data['descripcion']
        if 'imagen' in producto_data:
            producto['imagen'] = producto_data['imagen']
        if 'precio' in producto_data:
            producto['precio'] = int(producto_data['precio'])
        if 'stock' in producto_data:
            producto['stock'] = int(producto_data['stock'])

        affected_rows = ProductoModel.update_producto_patch(producto)

        if affected_rows == 1:
            return jsonify({'message': "Producto actualizado parcialmente"}), 200
        else:
            return jsonify({'message': "No se actualizó el producto"}), 500

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
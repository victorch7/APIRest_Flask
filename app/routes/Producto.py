from flask import Blueprint, jsonify, request
# Entities
from models.entities.Product import Producto
# Modelos
from models.ProductModel import ProductoModel

import uuid #Genera un codigo unico a partir de la fecha y hora del momento actual

main = Blueprint('producto_bp', __name__)

#Retorna todos los productos
@main.route('/')
def get_productos():
    try:
        productos = ProductoModel.get_productos()
        return jsonify(productos)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
#Retorna un solo producto con el id que se manda como petición
@main.route('/<id>')
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
@main.route('/add', methods=['POST'])
def add_producto():
    try:
        nombre = request.json['nombre']
        categoria = request.json['categoria']
        descripcion = request.json['descripcion']
        imagen = request.json['imagen']
        precio = int(request.json['precio'])
        stock = int(request.json['stock'])
        id = uuid.uuid4() #convierter a string porque es un objeto
        
        producto = Producto(str(id), nombre, categoria, descripcion, imagen, precio, stock)
        affected_rows = ProductoModel.add_producto(producto)
        
        if affected_rows == 1: #Si afecto una fila retorna el id del nuevo producto
            return jsonify(producto.id)
        else:
            return jsonify({'message': "Error al insertar"}), 500
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
#Editar un producto
@main.route('/update/<id>', methods=['PUT'])
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
            return jsonify(producto.id)
        else:
            return jsonify({'message': "No se actualizo el producto"}), 404

    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
    
#Eliminar un produto
@main.route('/delete/<id>', methods=['DELETE'])
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

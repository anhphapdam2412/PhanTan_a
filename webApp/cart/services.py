from flask import Flask, request, jsonify, session

def add_to_cart_service():
    data = request.get_json()
    if not data:
        return jsonify(success=False, message="Dữ liệu sản phẩm không hợp lệ"), 400

    product_id = int(data.get('id', 0))
    product_name = data.get('name')
    product_price = float(data.get('price', 0))
    image_url = data.get('image_url', '')

    if not product_id or not product_name:
        return jsonify(success=False, message="Thông tin sản phẩm không đầy đủ"), 400

    cart = _get_cart()

    # Kiểm tra sản phẩm đã tồn tại trong giỏ hàng chưa
    for item in cart:
        if 'id' in item and item['id'] == product_id:
            item['quantity'] += 1
            _update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])

    # Nếu sản phẩm chưa có, thêm mới vào giỏ hàng
    new_item = {
        'id': product_id,
        'name': product_name,
        'price': product_price,
        'quantity': 1,
        'image_url': image_url
    }
    cart.append(new_item)
    _update_cart(cart)
    return jsonify(success=True, new_quantity=1)

def remove_from_cart_service(product_id):
    cart = _get_cart()
    cart = [item for item in cart if item['id'] != product_id]
    _update_cart(cart)
    return jsonify(success=True)

def increase_quantity_service(product_id):
    cart = _get_cart()
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1
            _update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])
    return jsonify(success=False, message="Sản phẩm không tồn tại trong giỏ hàng"), 404

def decrease_quantity_service(product_id):
    cart = _get_cart()
    for item in cart:
        if item['id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1
            else:
                cart.remove(item)
            _update_cart(cart)
            return jsonify(success=True, new_quantity=item.get('quantity', 0))
    return jsonify(success=False, message="Sản phẩm không tồn tại trong giỏ hàng"), 404

def _get_cart():
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def _update_cart(cart):
    session['cart'] = cart
    session.modified = True
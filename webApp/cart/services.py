from flask import Flask, request, jsonify, session

def add_to_cart_service():
    """
    Thêm sản phẩm vào giỏ hàng hoặc tăng số lượng nếu sản phẩm đã có.
    """
    data = request.get_json()
    if not data:
        return jsonify(success=False, message="Dữ liệu sản phẩm không hợp lệ"), 400

    # Lấy thông tin sản phẩm từ request
    product_id = int(data.get('id', 0))  # ID sản phẩm
    product_name = data.get('name')  # Tên sản phẩm
    product_price = float(data.get('price', 0))  # Giá sản phẩm
    image_url = data.get('image_url', '')  # URL ảnh sản phẩm

    # Kiểm tra thông tin sản phẩm có hợp lệ không
    if not product_id or not product_name:
        return jsonify(success=False, message="Thông tin sản phẩm không đầy đủ"), 400

    cart = _get_cart()  # Lấy giỏ hàng từ session

    # Kiểm tra xem sản phẩm đã tồn tại trong giỏ hàng chưa
    for item in cart:
        if 'id' in item and item['id'] == product_id:
            # Nếu đã có, tăng số lượng sản phẩm
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
    """
    Xóa sản phẩm khỏi giỏ hàng.
    """
    cart = _get_cart()
    cart = [item for item in cart if item['id'] != product_id]  # Lọc ra sản phẩm cần xóa
    _update_cart(cart)
    return jsonify(success=True)

def increase_quantity_service(product_id):
    """
    Tăng số lượng sản phẩm trong giỏ hàng.
    """
    cart = _get_cart()
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] += 1  # Tăng số lượng
            _update_cart(cart)
            return jsonify(success=True, new_quantity=item['quantity'])
    return jsonify(success=False, message="Sản phẩm không tồn tại trong giỏ hàng"), 404

def decrease_quantity_service(product_id):
    """
    Giảm số lượng sản phẩm trong giỏ hàng. Nếu số lượng = 1 thì xóa sản phẩm.
    """
    cart = _get_cart()
    for item in cart:
        if item['id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1  # Giảm số lượng nếu lớn hơn 1
            else:
                cart.remove(item)  # Nếu chỉ còn 1 thì xóa sản phẩm
            _update_cart(cart)
            return jsonify(success=True, new_quantity=item.get('quantity', 0))
    return jsonify(success=False, message="Sản phẩm không tồn tại trong giỏ hàng"), 404

def _get_cart():
    """
    Lấy giỏ hàng từ session. Nếu chưa có thì khởi tạo danh sách rỗng.
    """
    if 'cart' not in session:
        session['cart'] = []
    return session['cart']

def _update_cart(cart):
    """
    Cập nhật giỏ hàng trong session và đánh dấu session đã bị thay đổi.
    """
    session['cart'] = cart
    session.modified = True

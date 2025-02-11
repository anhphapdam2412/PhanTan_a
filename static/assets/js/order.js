document.addEventListener('DOMContentLoaded', () => {
    // Hàm tải lại trang
    const reloadCart = () => location.reload();

    // Hàm hiển thị thông báo
    const showAlert = (message, isError = false) => {
        alert(isError ? `Lỗi: ${message}` : message);
    };

    // ---------------------------
    // Xử lý xóa sản phẩm khỏi giỏ hàng
    // ---------------------------
    const removeButtons = document.querySelectorAll('.cart_item-remove');
    removeButtons.forEach(btn => {
        btn.addEventListener('click', async (event) => {
            event.preventDefault();
            const productId = btn.dataset.id;
            if (!productId) {
                showAlert('ID sản phẩm không hợp lệ', true);
                return;
            }
            if (confirm('Bạn có chắc chắn muốn xóa sản phẩm này?')) {
                try {
                    const response = await fetch(`/cart/remove/${productId}`, { method: 'POST' });
                    const data = await response.json();
                    if (data.success) {
                        showAlert('Xóa sản phẩm thành công');
                        
                        // Xóa sản phẩm khỏi giao diện
                        const cartItem = btn.closest('.cart_item');
                        if (cartItem) {
                            cartItem.remove();
                        }

                        // Cập nhật lại tổng giá trị đơn hàng
                        const totalPriceElement = document.querySelector('.cart_total span');
                        if (totalPriceElement) {
                            let currentTotal = parseFloat(totalPriceElement.innerText.replace(/[^\d]/g, ''));
                            let productPrice = parseFloat(cartItem.querySelector('.cart_item-price').innerText.replace(/[^\d]/g, ''));
                            let productQuantity = parseInt(cartItem.querySelector('.cart_item-quantity-value').innerText);
                            totalPriceElement.innerText = `${(currentTotal - productPrice * productQuantity).toLocaleString()} VND`;
                        }

                        // Kiểm tra nếu giỏ hàng rỗng thì hiển thị thông báo
                        if (document.querySelectorAll('.cart_item').length === 0) {
                            document.querySelector('.cart_container').innerHTML = `<p class="cart_empty">Giỏ hàng trống. <a href="/products">Tiếp tục mua sắm</a></p>`;
                        }
                        
                    } else {
                        showAlert(data.message || 'Xóa sản phẩm thất bại', true);
                    }
                } catch (error) {
                    console.error('Lỗi khi xóa sản phẩm:', error);
                    showAlert('Có lỗi xảy ra khi xóa sản phẩm', true);
                }
            }
        });
    });

// ---------------------------
// Xử lý tăng/giảm số lượng sản phẩm
// ---------------------------
const handleQuantityChange = async (isIncrease, event) => {
    event.preventDefault();
    // Sử dụng event.currentTarget để lấy nút được click
    const btn = event.currentTarget;
    const productId = btn.dataset.id;
    if (!productId) {
        showAlert('ID sản phẩm không hợp lệ', true);
        return;
    }
    const endpoint = isIncrease ? 'increase' : 'decrease';
    try {
        const response = await fetch(`/cart/${endpoint}/${productId}`, { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            // Cập nhật số lượng trong giao diện nếu có element chứa số lượng (class .cart_item-quantity-value)
            const quantityElement = btn.parentElement.querySelector('.cart_item-quantity-value');
            if (quantityElement) {
                quantityElement.textContent = data.new_quantity;
                // Nếu số lượng giảm xuống 0, xóa dòng sản phẩm khỏi DOM
                if (data.new_quantity <= 0) {
                    const cartItem = btn.closest('.cart_item');
                    if (cartItem) {
                        cartItem.remove();
                    }
                }
            } else {
                // Nếu không tìm thấy phần tử cập nhật số lượng, reload trang
                reloadCart();
            }
        } else {
            showAlert(data.message || 'Cập nhật thất bại', true);
        }
    } catch (error) {
        console.error('Lỗi khi cập nhật số lượng:', error);
        showAlert('Có lỗi xảy ra khi cập nhật giỏ hàng', true);
    }
};

const increaseButtons = document.querySelectorAll('.quantity-increase');
increaseButtons.forEach(btn => {
    btn.addEventListener('click', (event) => {
        handleQuantityChange(true, event);
    });
});

const decreaseButtons = document.querySelectorAll('.quantity-decrease');
decreaseButtons.forEach(btn => {
    btn.addEventListener('click', (event) => {
        handleQuantityChange(false, event);
    });
});

// ---------------------------
// Xử lý thêm sản phẩm vào giỏ hàng (từ trang sản phẩm)
// ---------------------------
const addToCartButtons = document.querySelectorAll('.product_list-addtocart');
addToCartButtons.forEach(btn => {
    btn.addEventListener('click', async (event) => {
        event.preventDefault();
        const productId   = btn.dataset.id;
        const productName = btn.dataset.name;
        const productPrice = btn.dataset.price;
        const productImage = btn.dataset.image; // Trường image

        if (!productId || !productName || !productPrice) {
            showAlert('Thông tin sản phẩm không hợp lệ.', true);
            return;
        }
        try {
            const response = await fetch('/cart/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    id: productId, 
                    name: productName, 
                    price: parseFloat(productPrice),
                    image_url: productImage
                })
            });
            const data = await response.json();
            if (data.success) {
                showAlert('Thêm sản phẩm thành công');
                reloadCart();
            } else {
                showAlert(data.message || 'Thêm sản phẩm thất bại', true);
            }
        } catch (error) {
            console.error('Lỗi khi thêm sản phẩm:', error);
            showAlert('Có lỗi xảy ra khi thêm sản phẩm vào giỏ', true);
            showAlert(data.message);
        }

    });
});
});

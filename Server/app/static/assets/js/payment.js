document.addEventListener("DOMContentLoaded", function () {
    // Kiểm tra xem cartData có tồn tại và là mảng không
    if (typeof cartData === "undefined" || !Array.isArray(cartData)) {
        console.error("🚨 Lỗi: Không thể lấy dữ liệu giỏ hàng.");
        cartData = [];  // Đảm bảo cartData là mảng trống nếu có lỗi
    }

    const cartSummary = document.getElementById("cart-summary");
    const totalPrice = document.getElementById("total-price");
    let totalAmount = 0;

    // Kiểm tra giỏ hàng có trống không
    if (cartData.length === 0) {
        cartSummary.innerHTML = "<li>🛒 Giỏ hàng của bạn đang trống</li>";
    } else {
        cartSummary.innerHTML = "";  // Xóa nội dung cũ tránh bị lặp
        totalAmount = 0; // Đảm bảo tổng tiền bắt đầu từ 0
    
        cartData.forEach(item => {
            const listItem = document.createElement("li");
            listItem.textContent = `${item.name} x${item.quantity} - ${(item.price * item.quantity).toLocaleString("vi-VN")} VND`;
            cartSummary.appendChild(listItem);
    
            totalAmount += item.price * item.quantity;
        });
    
        console.log("Tổng tiền:", totalAmount); // Kiểm tra trong console
    }
    
    totalPrice.textContent = totalAmount.toLocaleString("vi-VN");

    // Xử lý sự kiện thanh toán
    const paymentForm = document.getElementById("payment-form");
    if (paymentForm) {
        paymentForm.addEventListener("submit", function (event) {
            event.preventDefault();  // Ngừng hành động mặc định của form

            const name = document.getElementById("name").value.trim();
            const phone = document.getElementById("phone").value.trim();
            const address = document.getElementById("address").value.trim();
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked');

            // Kiểm tra dữ liệu nhập vào có đầy đủ không
            if (!name || !phone || !address || !paymentMethod) {
                alert("⚠️ Vui lòng nhập đầy đủ thông tin thanh toán.");
                return;
            }

            // Gửi dữ liệu thanh toán lên server
            fetch("/payment/submit", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: name,
                    phone: phone,
                    address: address,
                    payment_method: paymentMethod.value,
                    cart: cartData
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`✅ Thanh toán thành công! Tổng tiền: ${data.total_price.toLocaleString("vi-VN")}`);
                    window.location.href = "/";  // Chuyển về trang chủ sau khi thanh toán thành công
                } else {
                    alert(data.message || "❌ Thanh toán thất bại.");
                }
            })
            .catch(error => {
                console.error("Lỗi khi thanh toán:", error);
                alert("⚠️ Có lỗi xảy ra khi thanh toán. Vui lòng thử lại.");
            });
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const path = window.location.pathname; // Lấy đường dẫn trang hiện tại

    const cartStep = document.querySelector('.cart_header-cart');
    const paymentStep = document.querySelector('.cart_header-payment');
    const successStep = document.querySelector('.cart_header-success');

    // Reset lại tất cả về màu xám trước
    if (cartStep) cartStep.style.color = "#cccccc";
    if (paymentStep) paymentStep.style.color = "#cccccc";
    if (successStep) successStep.style.color = "#cccccc";

    // Xác định trang hiện tại và đổi màu tương ứng
    if (path.includes("/cart")) {
        if (cartStep) cartStep.style.color = "black"; // Trang giỏ hàng
    } else if (path.includes("/payment")) {
        if (paymentStep) paymentStep.style.color = "black"; // Trang thanh toán
    } else if (path.includes("/success")) {
        if (successStep) successStep.style.color = "black"; // Trang hoàn tất
    }
});

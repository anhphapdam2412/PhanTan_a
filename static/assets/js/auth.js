const loginBtn = document.querySelector('.js_login'); 
const modal = document.querySelector('.js_modal'); 
const modalClose = document.querySelectorAll('.js_modal-close'); 
const modalOverlay = document.querySelector('.js_overlay'); 
const loginForm = document.querySelector('.js_login-form');
const registerForm = document.querySelector('.js_register-form');
const switchToRegisterButtons = document.querySelectorAll('.js_switch');
const loginButton = document.querySelector('.btn_login');
const registerButton = document.querySelector('.btn_register');
const logoutButton = document.querySelector('.js_logout');

function showLoginForm() {
    modal.classList.add('open');
}

function closeModal() {
    modal.classList.remove('open');
}

function handleLogin(event) {
    event.preventDefault();

    const username = document.querySelector('.auth_form-input[type="text"]').value;
    const password = document.querySelector('.auth_form-input[type="password"]').value;

    if (!username || !password) {
        alert("Vui lòng điền đầy đủ thông tin!");
        return;
    }

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (response.ok) { // Nếu mã phản hồi là 200-299
            return response.json().then(data => {
                setCookie('username', username, 1);
                location.reload(); // Reload lại trang sau khi đăng nhập thành công
            });
        } else { // Xử lý lỗi với mã phản hồi khác
            return response.json().then(data => {
                alert(data.message);
            });
        }
    })
    .catch(error => {
        alert('Lỗi kết nối server, vui lòng thử lại sau!');
        console.error('Lỗi kết nối:', error.message);
    });
}

function handleRegister(event) {
    event.preventDefault();

    const username = registerForm.querySelector('input[type="text"]').value;
    const password = registerForm.querySelector('input[type="password"]').value;
    const confirmPassword = registerForm.querySelectorAll('input[type="password"]')[1].value;

    if (!username || !password || !confirmPassword) {
        alert("Vui lòng nhập đầy đủ thông tin đăng ký!");
        return;
    }

    if (password !== confirmPassword) {
        alert("Mật khẩu xác nhận không khớp!");
        return;
    }

    fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message || "Đăng ký thất bại!");
            });
        }
        return response.json();
    })
    .then(data => {
        alert("Đăng ký thành công! Vui lòng đăng nhập.");
        location.reload(); // Reload lại trang sau khi đăng ký
    })
    .catch(error => alert(error.message));
}

loginButton.addEventListener('click', handleLogin);
registerButton.addEventListener('click', handleRegister);

loginBtn.addEventListener('click', showLoginForm);
logoutButton.addEventListener('click', handleLogout);
modalOverlay.addEventListener('click', closeModal);
modalClose.forEach(button => button.addEventListener('click', closeModal));

// Chuyển đổi giữa form đăng nhập và đăng ký
switchToRegisterButtons.forEach(button => {
    button.addEventListener('click', () => {
        const loginForm = document.querySelector('.js_login-form');
        if (loginForm.style.display === 'block') {
            loginForm.style.display = 'none';
            registerForm.style.display = 'block';
        } else {
            registerForm.style.display = 'none';
            loginForm.style.display = 'block';
        }
    });
});


function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function getCookie(name) {
    return document.cookie.split('; ').find(row => row.startsWith(name))?.split('=')[1];
}

function displayUsername(username) {
    const loginBtnContainer = document.querySelector('.js_login button');
    const loginForm = document.querySelector('.js_login');
    if (loginBtnContainer && loginForm) {
        loginBtnContainer.textContent = `Xin chào, ${username}`;
        loginBtnContainer.style.fontSize = '10px';
        loginForm.style.pointerEvents = 'none';
    }
}

function handleLogout() {
    setCookie('username', '', -1); // Xóa cookie bằng cách đặt thời gian hết hạn âm
    location.reload(); // Reload lại trang để cập nhật trạng thái đăng xuất
}

document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.querySelector('.js_logout');
    const username = getCookie('username');

    // Ẩn nút Đăng xuất nếu chưa đăng nhập
    if (!username && logoutButton) {
        logoutButton.style.display = 'none';
    }
    if (username) {
        displayUsername(username);
    }
});
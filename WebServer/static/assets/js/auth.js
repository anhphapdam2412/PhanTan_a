const loginBtn = document.querySelector('.js_login'); 
const modal = document.querySelector('.js_modal'); 
const modalClose = document.querySelectorAll('.js_modal-close'); 
const modalOverlay = document.querySelector('.js_overlay'); 

function showLoginForm() {
    modal.classList.add('open');
}

function closeModal() {
    modal.classList.remove('open');
}

loginBtn.addEventListener('click', showLoginForm);
modalOverlay.addEventListener('click', closeModal);     
modalClose.forEach(button => button.addEventListener('click', closeModal));
document.querySelector('.btn_login-register').addEventListener('click', handleLogin);

function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function getCookie(name) {
    return document.cookie.split('; ').find(row => row.startsWith(name))?.split('=')[1];
}

function handleLogin(event) {
    event.preventDefault();

    const username = document.querySelector('.auth_form-input[type="text"]').value;
    const password = document.querySelector('.auth_form-input[type="password"]').value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Sai thông tin đăng nhập!');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("Đăng nhập thành công!");
            setCookie('username', username, 1); // Lưu thông tin vào cookie
            displayUsername(username);
        }
    })
    .catch(error => alert(error.message));
}

// Hiển thị trạng thái online
function showOnlineStatus(username) {
    const onlineStatus = document.createElement('div');
    onlineStatus.id = 'online-status';
    onlineStatus.style.backgroundColor = '#4CAF50';
    onlineStatus.style.color = 'white';
    onlineStatus.style.padding = '10px';
    onlineStatus.style.position = 'fixed';
    onlineStatus.style.top = '10px';
    onlineStatus.style.left = '10px';
    onlineStatus.style.borderRadius = '5px';
    onlineStatus.style.fontSize = '16px';
    onlineStatus.textContent = `Online: ${username}`;
    onlineStatus.style.zIndex = -1;

    document.body.appendChild(onlineStatus);
}
function notifyServer(username) {
    fetch('/notify-login-success', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: username })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Thông báo đã được gửi đến server.");
    })
    .catch(error => {
        console.error("Lỗi khi gửi thông báo về server:", error);
    });
}
function displayUsername(username) {
    if (loginBtn) {
        loginBtn.style.display = 'none';
        const userDisplay = document.createElement('div');
        userDisplay.textContent = `${username}`;
        userDisplay.style.color = '#4CAF50';
        userDisplay.style.fontWeight = 'bold';
        loginBtn.parentElement.appendChild(userDisplay);
    }
}
// Khởi tạo nút đăng xuất và thêm vào DOM sau khi đăng nhập thành công
function handleSuccessfulLogin(username) {
    loginBtn.style.display = 'none';  // Ẩn nút đăng nhập
    displayLogoutButton();            // Hiện nút đăng xuất
    showOnlineStatus(username);       // Hiển thị trạng thái online
}

function displayUsername(username) {
    const loginBtn = document.querySelector('.js_login');
    if (loginBtn) {
        loginBtn.style.display = 'none'; // Ẩn nút đăng nhập

        // Tạo phần tử hiển thị tên tài khoản và nút đăng xuất
        const userDisplay = document.createElement('div');
        userDisplay.classList.add('user-display-container');
        userDisplay.style.display = 'flex';
        userDisplay.style.alignItems = 'center';
        userDisplay.style.marginLeft = '10px';

        const userText = document.createElement('span');
        userText.textContent = `Xin chào, ${username}`;
        userText.style.color = '#4CAF50';
        userText.style.fontWeight = 'bold';

        const logoutBtn = document.createElement('button');
        logoutBtn.textContent = 'Đăng xuất';
        logoutBtn.style.marginLeft = '10px';
        logoutBtn.style.backgroundColor = '#f44336';
        logoutBtn.style.color = 'white';
        logoutBtn.style.padding = '5px 10px';
        logoutBtn.style.border = 'none';
        logoutBtn.style.borderRadius = '5px';
        logoutBtn.style.cursor = 'pointer';

        logoutBtn.addEventListener('click', handleLogout);

        userDisplay.appendChild(userText);
        userDisplay.appendChild(logoutBtn);

        // Thêm vào vị trí cũ của nút đăng nhập
        loginBtn.parentElement.appendChild(userDisplay);
    }
}

function handleLogout() {
    fetch('/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        }
    })
    .catch(error => {
        console.error("Lỗi khi đăng xuất:", error);
        alert("Không thể đăng xuất!");
    });
}
window.onload = function () {
    const username = getCookie('username');
    if (username) {
        displayUsername(decodeURIComponent(username));
    }
};
window.onload = function () {
    fetch('/session-info')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                displayUsername(data.username);
            }
        });
};
function switchForm() {
    if (loginForm.style.display === 'block') {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    } else {
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
    }
}

const registerForm = document.querySelector('.js_register-form');
const registerButton = registerForm.querySelector('.btn_login-register');
const switchToRegisterButtons = document.querySelectorAll('.js_switch');

function handleRegister(event) {
    event.preventDefault();

    const email = registerForm.querySelector('input[type="text"]').value;
    const password = registerForm.querySelector('input[type="password"]').value;
    const confirmPassword = registerForm.querySelectorAll('input[type="password"]')[1].value;

    if (!email || !password || !confirmPassword) {
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
        body: JSON.stringify({ email, password })
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
        closeModal(); // Close the register modal after success
    })
    .catch(error => alert(error.message));
}

// Switching between forms
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

// Handle register button click
registerButton.addEventListener('click', handleRegister);
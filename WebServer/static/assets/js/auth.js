// Chọn các phần tử cần thao tác
const loginBtn = document.querySelector('.js_login');
const modal = document.querySelector('.js_modal');
const modalClose = document.querySelectorAll('.js_modal-close');
const modalOverlay = document.querySelector('.js_overlay');
const switchToRegister = document.querySelectorAll('.js_switch');
const loginForm = document.querySelector('.js_login-form');
const registerForm = document.querySelector('.js_register-form');
const registerBtn = document.querySelector('.btn_register-submit');

// Hiển thị form đăng nhập
function showLoginForm() {
    modal.classList.add('open');
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
}

// Đóng modal
function closeModal() {
    modal.classList.remove('open');
}

// Chuyển đổi giữa form đăng nhập và đăng ký
function switchForm() {
    if (loginForm.style.display === 'block') {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    } else {
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
    }
}

// Cài đặt cookie
function setCookie(name, value, days) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

// Lấy cookie
function getCookie(name) {
    return document.cookie.split('; ').find(row => row.startsWith(name))?.split('=')[1];
}

// Xử lý đăng nhập
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
        if (!response.ok) throw new Error('Sai thông tin đăng nhập!');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("Đăng nhập thành công!");
            setCookie('username', username, 1);
            handleSuccessfulLogin(username);
        }
    })
    .catch(error => alert(error.message));
}

// Hiển thị trạng thái online
function showOnlineStatus(username) {
    let onlineStatus = document.querySelector('#online-status');
    if (!onlineStatus) {
        onlineStatus = document.createElement('div');
        onlineStatus.id = 'online-status';
        onlineStatus.style.backgroundColor = '#4CAF50';
        onlineStatus.style.color = 'white';
        onlineStatus.style.padding = '10px';
        onlineStatus.style.position = 'fixed';
        onlineStatus.style.bottom = '10px';
        onlineStatus.style.right = '10px';
        onlineStatus.style.borderRadius = '5px';
        onlineStatus.style.fontSize = '16px';
        onlineStatus.textContent = `Trạng thái: Online (${username})`;
        document.body.appendChild(onlineStatus);
    }
}

// Thông báo về server khi đăng nhập thành công
function notifyServer(username) {
    fetch('/notify-login-success', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username })
    })
    .then(response => response.json())
    .then(() => console.log("Thông báo đã được gửi đến server."))
    .catch(error => console.error("Lỗi khi gửi thông báo về server:", error));
}

// Hiển thị tên người dùng và thêm nút đăng xuất
function displayUsername(username) {
    if (loginBtn) {
        loginBtn.style.display = 'none';
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
        loginBtn.parentElement.appendChild(userDisplay);
    }
}

// Xử lý nút đăng xuất
function handleLogout() {
    fetch('/logout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            document.cookie = "username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            location.reload();
        }
    })
    .catch(error => {
        console.error("Lỗi khi đăng xuất:", error);
        alert("Không thể đăng xuất!");
    });
}

// Kiểm tra trạng thái phiên từ server
function checkSessionFromServer() {
    fetch('/session-info')
        .then(response => response.json())
        .then(data => {
            if (data.logged_in) {
                handleSuccessfulLogin(data.username);
            }
        })
        .catch(error => console.error("Lỗi khi kiểm tra phiên:", error));
}

// Xử lý sau khi đăng nhập thành công
function handleSuccessfulLogin(username) {
    displayUsername(username);
    showOnlineStatus(username);
    notifyServer(username);
}

// Gán sự kiện cho các nút và biểu mẫu
loginBtn?.addEventListener('click', showLoginForm);
modalOverlay?.addEventListener('click', closeModal);
modalClose.forEach(button => button.addEventListener('click', closeModal));
document.querySelector('.btn_login-submit')?.addEventListener('click', handleLogin);
switchToRegister.forEach(button => button.addEventListener('click', switchForm));

// Kiểm tra trạng thái khi tải trang
window.addEventListener('DOMContentLoaded', () => {
    const username = getCookie('username');
    if (username) {
        handleSuccessfulLogin(decodeURIComponent(username));
    } else {
        checkSessionFromServer();
    }
});

// Xử lý sự kiện đăng ký
function handleRegister(event) {
    event.preventDefault();

    const username = document.querySelector('.js_register-username').value;
    const password = document.querySelector('.js_register-password').value;

    if (!username || !password) {
        alert("Vui lòng nhập đầy đủ thông tin!");
        return;
    }

    fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Đăng ký thành công!");
            closeModal();
        } else {
            alert(data.message || "Đăng ký thất bại!");
        }
    })
    .catch(error => {
        console.error("Lỗi khi đăng ký:", error);
        alert("Có lỗi xảy ra, vui lòng thử lại sau.");
    });
}

// Gán sự kiện cho nút đăng ký
registerBtn?.addEventListener('click', handleRegister);

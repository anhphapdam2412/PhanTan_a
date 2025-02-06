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

function handleLogin(event) {
    event.preventDefault();

    const username = document.querySelector('.auth_form-input[type="text"]').value;
    const password = document.querySelector('.auth_form-input[type="password"]').value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Đăng nhập thành công!");

            // Hiển thị thông báo "Online"
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
            onlineStatus.textContent = 'Online';

            document.body.appendChild(onlineStatus); // Thêm vào body của trang

            // Ẩn thông báo sau 3 giây
            setTimeout(() => {
                onlineStatus.style.display = 'none';
            }, 3000);

            // Gửi thông báo về server rằng người dùng đã đăng nhập thành công
            notifyServer(username);

        } else {
            alert("Sai thông tin đăng nhập!");
        }
    })
    .catch(error => console.error("Lỗi:", error));
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
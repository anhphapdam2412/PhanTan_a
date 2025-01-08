const loginBtn = document.querySelector('.js_login'); 
const modal = document.querySelector('.js_modal'); 
const modalClose = document.querySelectorAll('.js_modal-close'); 
const modalOverlay = document.querySelector('.js_overlay'); 
const switchBtns = document.querySelectorAll('.auth_form-switch'); 
const loginForm = document.querySelector('.js_login-form'); 
const registerForm = document.querySelector('.js_register-form'); 

function showLoginForm() {
    modal.classList.add('open');
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
}
function switchForm() {
    if (loginForm.style.display === 'block') {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
    } else {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    }
}
function handleBackButton() {
    if (registerForm.style.display === 'block') {
        // Nếu đang ở form đăng ký, chuyển về form đăng nhập
        registerForm.style.display = 'none';
        loginForm.style.display = 'block';
    } else {
        // Nếu đang ở form đăng nhập, đóng modal
        modal.classList.remove('open');
    }
}
function closeModal() {
    modal.classList.remove('open');
}

loginBtn.addEventListener('click', showLoginForm);
modalClose.forEach(button => button.addEventListener('click', handleBackButton));
modalOverlay.addEventListener('click', closeModal);     
switchBtns.forEach(button => button.addEventListener('click', switchForm));

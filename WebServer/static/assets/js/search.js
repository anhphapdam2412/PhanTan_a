const searchBtn = document.querySelector('.header_navbar-btn-item.search-btn');
const searchContainer = document.querySelector('.header_navbar-search');

// Hiện thanh tìm kiếm khi di chuột vào nút tìm kiếm
searchBtn.addEventListener('mouseenter', () => {
    searchContainer.style.display = 'block'; // Hiển thị thanh tìm kiếm
});

// Ẩn thanh tìm kiếm khi di chuột ra khỏi nút tìm kiếm
searchBtn.addEventListener('mouseleave', () => {
    searchContainer.style.display = 'none'; // Ẩn thanh tìm kiếm
});

// Giữ thanh tìm kiếm hiển thị khi di chuột vào nó
searchContainer.addEventListener('mouseenter', () => {
    searchContainer.style.display = 'block'; // Hiển thị thanh tìm kiếm
});

// Ẩn thanh tìm kiếm khi di chuột ra khỏi thanh tìm kiếm
searchContainer.addEventListener('mouseleave', () => {
    searchContainer.style.display = 'none'; // Ẩn thanh tìm kiếm
});

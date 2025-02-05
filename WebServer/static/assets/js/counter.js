const minusBtn = document.querySelector('.js_minus');
const plusBtn = document.querySelector('.js_plus');
const inputNumber = document.querySelector('.js_count_value');

minusBtn.addEventListener('click', () => {
    let currentValue = parseInt(inputNumber.value);
    if (currentValue > 1) {
        currentValue--;
        inputNumber.value = currentValue;
    }
});

plusBtn.addEventListener('click', () => {
    let currentValue = parseInt(inputNumber.value);
    currentValue++;
    inputNumber.value = currentValue;
});

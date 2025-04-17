document.addEventListener("DOMContentLoaded", () => {
    
    document.addEventListener('add-to-cart', (event) => {
        const qty_circle = document.querySelector('.qty-circle');
        qty_circle.innerHTML = '1';
    })

    document.addEventListener('clear-cart', (event) => {
        const qty_circle = document.querySelector('.qty-circle');
        qty_circle.innerHTML = '';
    })

    const check_condition = document.getElementById('condition-check');
    const payment_btn = document.querySelector('.payment-submit');
    if (check_condition && payment_btn) {
        if (!check_condition.checked) {
            payment_btn.disabled = true;
        }

        check_condition.addEventListener('change', (event) => {
            if (event.currentTarget.checked) {
                payment_btn.disabled = false;
            } else {
                payment_btn.disabled = true;
            }
          })
    }
});
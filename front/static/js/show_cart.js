document.addEventListener("DOMContentLoaded", () => {
    
    const clear_cart_btn = document.querySelector('.clear-offer');
    clear_cart_btn.addEventListener('click', (event) => {
        clearCart()
    });

    document.addEventListener('clear-cart', (event) => {
        const cart_box = document.querySelector('.cart-box');
        const empty_cart_box = document.querySelector('.empty-cart-box');

        cart_box.style.display = 'none';
        empty_cart_box.style.display = 'block';
    })
});
document.addEventListener("DOMContentLoaded", () => {
    
    const add_cart_btns = document.getElementsByClassName('add-cart-btn');
    if (add_cart_btns) {
        for (let i = 0; i < add_cart_btns.length; i++) {
            add_cart_btns[i].addEventListener('click', (event) => {

                let button = add_cart_btns[i];
                let offer_id = button.getAttribute('data-offer-id');

                addToCart(offer_id, '1');
            })
        }
    }

    document.addEventListener('add-to-cart', (event) => {

        const offer_id = event.detail.cart.offer;
        
        const old_selected_card = document.querySelector('.card.selected');
        const old_selected_btn = document.querySelector('.btn.disabled');
        const new_selected_card = document.querySelector(`.card[data-offer-id="${offer_id}"]`);
        const new_selected_btn = document.querySelector(`button[data-offer-id="${offer_id}"]`)

        if (old_selected_card && old_selected_btn) {
            old_selected_card.classList.remove('selected');
            old_selected_btn.classList.remove('disabled', 'btn-outline-success');
            old_selected_btn.classList.add('btn-outline-primary')
            old_selected_btn.disabled = false;
            new_selected_card.classList.add('selected');
            new_selected_btn.classList.add('disabled', 'btn-outline-success');
            new_selected_btn.classList.remove('btn-outline-primary');
            new_selected_btn.disabled = true;

        } else {
            new_selected_card.classList.add('selected');
            new_selected_btn.classList.add('disabled', 'btn-outline-success');
            new_selected_btn.classList.remove('btn-outline-primary');
            new_selected_btn.disabled = true;
        }
    });
});
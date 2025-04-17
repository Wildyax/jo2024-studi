/**
 * Add an offer to the cart
 * @param {string} offer_id 
 */
function addToCart(offer_id) {
    
    fetch(`/add-to-cart?offer_id=${offer_id}`, {
        headers: { 
            "X-Requested-with": "XMLHttpRequest" 
        }
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP : ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                const event = new CustomEvent('add-to-cart', {'detail': {'cart': data.cart}});
                document.dispatchEvent(event);
            } 
        })
        .catch((error) => {
            console.log(`Error while adding offer to cart : ${error}`);
        });
}

/**
 * Clear the cart
 */
function clearCart() {
    fetch(`/clear-cart`, {
        headers: { 
            "X-Requested-with": "XMLHttpRequest" 
        }
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP : ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                const event = new CustomEvent('clear-cart');
                document.dispatchEvent(event);
            } 
        })
        .catch((error) => {
            console.log(`Error while clearing cart : ${error}`);
        });
}
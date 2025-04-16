document.addEventListener("DOMContentLoaded", () => {
    const edit_offer_btn = document.getElementsByClassName('edit_btn');
    const save_offer_btn = document.getElementById('save-offer-btn');
    const remove_offer_btn = document.getElementsByClassName('remove_btn');
    
    if (edit_offer_btn) {
        for (let i = 0; i < edit_offer_btn.length; i++) {
            setEditBtnEvent(edit_offer_btn[i]);
        }
    }

    if (remove_offer_btn) {
        for (let i = 0; i < remove_offer_btn.length; i++) {
            setRemoveBtnEvent(remove_offer_btn[i]);
        }
    }

    if (save_offer_btn) {
        save_offer_btn.addEventListener('click', (event) => {
            saveOffer();
        })
    }
});

// Set event when edit button is clicked
function setEditBtnEvent(btn) {
    btn.addEventListener('click', (event) => {
        loadOfferEditForm(btn);
    });
}

// Set event when remove button is clicked
function setRemoveBtnEvent(btn) {
    btn.addEventListener('click', (event) => {
        removeOffer(btn);
    });
}


// Change form in the modal depend on which offer is selected
function loadOfferEditForm(btn) {
    const modal_body = document.getElementById('editOfferModalBody');
    const modal_title = document.getElementById('editOfferModalLabel');
    const offer_id = btn.getAttribute('data-offer-id');

    fetch('/back-office/offers/edit?offer-id=' + offer_id, {
        headers: { 
            "X-Requested-with": "XMLHttpRequest" 
        }
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Erreur HTTP : ${response.status}`);
            }
            return response.text();
        })
        .then((text) => {
            modal_body.innerHTML = text;
            Number(offer_id) < 1 ? modal_title.innerHTML = 'Ajouter une offre' : modal_title.innerHTML = 'Modifier une offre';
            addImagePreview()
        })
        .catch((error) => {
            console.log(`Error while getting offer form : ${error}`);
        });
}

// Add a preview when user select a new image for offer
function addImagePreview() {
    const imageInput = document.querySelector('input[type="file"][name="image"]');
    const imagePreview = document.getElementById('image-preview');

    if (imageInput && imagePreview) {
        imageInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (evt) {
                    imagePreview.src = evt.target.result;
                    imagePreview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                imagePreview.src = '';
                imagePreview.style.display = 'none';
            }
        });
    }
}

// Save an offer to database
function saveOffer() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const offer_edit_form = document.getElementById('offer-edit-form');
    const modal_body = document.getElementById('editOfferModalBody');
    const form_data = new FormData(offer_edit_form);
    const offers_row = document.getElementById('offers-row');
    const hidden_offer_id = document.querySelector('[name="offer-id"]');

    fetch('/back-office/offers/save', {
        method: 'POST',
        credentials: 'same-origin',
        body: form_data,
        headers: { 
            "X-Requested-with": "XMLHttpRequest", 
            "X-CSRFToken": csrftoken,
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
                modal_body.prepend(createSuccessDiv('L\'offre a été sauvegardée avec succés !'));

                const parser = new DOMParser();
                const doc = parser.parseFromString(data.card_html, 'text/html');
                const newCard = doc.body.firstChild;
                if (data.new) {
                    setEditBtnEvent(newCard.querySelector('.edit_btn'));
                    setRemoveBtnEvent(newCard.querySelector('.remove_btn'));
                    offers_row.append(newCard);
                    hidden_offer_id.value = data.offer_id;
                } else {
                    const card_element = document.querySelector('.col-card[data-offer-id="' + data.offer_id + '"]');
                    card_element.replaceWith(newCard);
                }
            } else {
                modal_body.prepend(createErrorDiv('Une erreur est survenue lors de la sauvegarde'));
            }
        })
        .catch((error) => {
            console.log(`Error while saving offer : ${error}`);
        });
}

// Remove an offer from database
function removeOffer(btn) {
    if (confirm('Êtes vous sûr de vouloir supprimer cette offre ?')) {
        const offer_id = btn.getAttribute('data-offer-id');

        fetch('/back-office/offers/delete?offer-id=' + offer_id, {
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
                    const card_element = document.querySelector('.col-card[data-offer-id="' + offer_id + '"]');
                    card_element.remove();
                }
            })
            .catch((error) => {
                console.log(`Error while getting offer form : ${error}`);
            });
    }
}

// Create a success div
function createSuccessDiv(text, replace=true) {
    if (replace) {
        const alert_div = document.getElementsByClassName('alert');
        for (let i = 0; i < alert_div.length; i++) {
            alert_div[i].remove()
        }
    }
    
    let success_div = document.createElement('div');
    success_div.classList.add('alert', 'alert-success', 'alert-dismissible', 'fade', 'show');
    success_div.setAttribute('role', 'alert');
    
    let success_text = document.createElement('div');
    success_text.insertAdjacentHTML('afterbegin', text);

    let close_btn = document.createElement('button');
    close_btn.classList.add('btn-close');
    close_btn.setAttribute('type', 'button');
    close_btn.setAttribute('data-bs-dismiss', 'alert');
    close_btn.setAttribute('aria-label', 'Close');

    success_div.append(success_text);
    success_div.append(close_btn);

    return success_div;
}

// Create an error div
function createErrorDiv(text, replace=true) {
    if (replace) {
        const alert_div = document.getElementsByClassName('alert');
        for (let i = 0; i < alert_div.length; i++) {
            alert_div[i].remove()
        }
    }
    
    let success_div = document.createElement('div');
    success_div.classList.add('alert', 'alert-danger', 'alert-dismissible', 'fade', 'show');
    success_div.setAttribute('role', 'alert');
    
    let success_text = document.createElement('div');
    success_text.insertAdjacentHTML('afterbegin', text);

    let close_btn = document.createElement('button');
    close_btn.classList.add('btn-close');
    close_btn.setAttribute('type', 'button');
    close_btn.setAttribute('data-bs-dismiss', 'alert');
    close_btn.setAttribute('aria-label', 'Close');

    success_div.append(success_text);
    success_div.append(close_btn);

    return success_div;
}
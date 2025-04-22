document.addEventListener("DOMContentLoaded", () => {
    
    const check_condition = document.getElementById('policy-checkbox');
    const subscribe_btn = document.querySelector('.submit-btn');
    if (check_condition && subscribe_btn) {
        if (!check_condition.checked) {
            subscribe_btn.disabled = true;
        }

        check_condition.addEventListener('change', (event) => {
            if (event.currentTarget.checked) {
                subscribe_btn.disabled = false;
            } else {
                subscribe_btn.disabled = true;
            }
          })
    }
});
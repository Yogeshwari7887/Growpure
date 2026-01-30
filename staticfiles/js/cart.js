document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            let productType = this.getAttribute("data-type");
            let productId = this.getAttribute("data-id");

            fetch(`/add-to-cart/${productType}/${productId}/`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    showPopup(data.message);
                    updateCartCount(data.cart_count);
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});

function showPopup(message) {
    let popup = document.createElement("div");
    popup.className = "cart-popup";
    popup.innerHTML = `<span>${message}</span>`;

    document.body.appendChild(popup);

    setTimeout(() => {
        popup.style.opacity = "0";
        setTimeout(() => popup.remove(), 500);
    }, 2000);
}

function updateCartCount(count) {
    let cartCounter = document.getElementById("cart-counter");
    if (cartCounter) {
        cartCounter.innerText = count;
    }
}

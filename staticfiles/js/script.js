// 'use strict';



// /**
//  * navbar toggle
//  */

const navOpenBtn = document.querySelector("[data-nav-open-btn]");
const navbar = document.querySelector("[data-navbar]");
const navCloseBtn = document.querySelector("[data-nav-close-btn]");

const navElems = [navOpenBtn, navCloseBtn];

for (let i = 0; i < navElems.length; i++) {
  navElems[i].addEventListener("click", function () {
    navbar.classList.toggle("active");
  });
}



/**
 * search toggle
 */

const searchContainer = document.querySelector("[data-search-wrapper]");
const searchBtn = document.querySelector("[data-search-btn]");

searchBtn.addEventListener("click", function () {
  searchContainer.classList.toggle("active");
});



/**
 * whishlist & cart toggle
 */

const panelBtns = document.querySelectorAll("[data-panel-btn]");
const sidePanels = document.querySelectorAll("[data-side-panel]");

for (let i = 0; i < panelBtns.length; i++) {
  panelBtns[i].addEventListener("click", function () {

    let clickedElemDataValue = this.dataset.panelBtn;

    for (let i = 0; i < sidePanels.length; i++) {

      if (clickedElemDataValue === sidePanels[i].dataset.sidePanel) {
        sidePanels[i].classList.toggle("active");
      } else {
        sidePanels[i].classList.remove("active");
      }

    }

  });
}



/**
 * back to top
 */

const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", function () {
  window.scrollY >= 100 ? backTopBtn.classList.add("active")
    : backTopBtn.classList.remove("active");
});



/**
 * product details page
 */

const productDisplay = document.querySelector("[data-product-display]");
const productThumbnails = document.querySelectorAll("[data-product-thumbnail]");

for (let i = 0; i < productThumbnails.length; i++) {
  productThumbnails[i].addEventListener("click", function () {
    productDisplay.src = this.src;
    productDisplay.classList.add("fade-anim");

    setTimeout(function () {
      productDisplay.classList.remove("fade-anim");
    }, 250);

  });
}

/**
 * search
 */

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector(".search-input");
  const searchSubmit = document.querySelector(".search-submit");
  const productList = document.querySelectorAll(".product-card");
  const productContainer = document.querySelector(".grid-list"); // Updated from "product-list" to "grid-list"

  function filterProducts() {
    const query = searchInput.value.trim().toLowerCase();
    let found = false;

    productList.forEach((product) => {
      const productName = product.querySelector(".card-title a").textContent.trim().toLowerCase();

      if (productName.includes(query)) {
        product.parentElement.style.display = "block"; // Show matching products
        found = true;
      } else {
        product.parentElement.style.display = "none"; // Hide unmatched products
      }
    });

    // Remove existing "Item not found" message if any
    const notFoundMessage = document.querySelector(".not-found");
    if (notFoundMessage) {
      notFoundMessage.remove();
    }

    // If no product is found, display a message
    if (!found) {
      const message = document.createElement("li");
      message.className = "not-found";
      message.textContent = "❌ Item not found";
      message.style.color = "red";
      message.style.textAlign = "center";
      message.style.padding = "10px";
      productContainer.appendChild(message);
    }
  }

  // Event Listeners
  searchSubmit.addEventListener("click", filterProducts);
  searchInput.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      filterProducts();
    }
  });
});


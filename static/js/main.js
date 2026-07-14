document.addEventListener("DOMContentLoaded", function () {
    // Hamburger menu
    const hamburger = document.querySelector(".hamburger");
    if (hamburger) {
        hamburger.addEventListener("click", function () {
            document.querySelector(".navbar").classList.toggle("mobile-open");
        });
    }

    // Swiper: Hero carousel
    if (document.querySelector(".hero-swiper")) {
        new Swiper(".hero-swiper", {
            loop: true,
            autoplay: { delay: 4500, disableOnInteraction: false },
            effect: "fade",
            fadeEffect: { crossFade: true },
            pagination: { el: ".hero-swiper .swiper-pagination", clickable: true },
            navigation: { nextEl: ".hero-swiper .swiper-button-next", prevEl: ".hero-swiper .swiper-button-prev" },
        });
    }

    // Swiper: Product rows
    document.querySelectorAll(".product-row.swiper").forEach(function (el) {
        new Swiper(el, {
            slidesPerView: 2,
            spaceBetween: 14,
            navigation: { nextEl: el.parentElement.querySelector(".swiper-button-next"), prevEl: el.parentElement.querySelector(".swiper-button-prev") },
            breakpoints: { 480: { slidesPerView: 2 }, 768: { slidesPerView: 3 }, 1024: { slidesPerView: 4 }, 1200: { slidesPerView: 5 } },
        });
    });

    // Swiper: Brand row
    if (document.querySelector(".brand-row.swiper")) {
        new Swiper(".brand-row.swiper", {
            slidesPerView: 3,
            spaceBetween: 12,
            breakpoints: { 480: { slidesPerView: 3 }, 768: { slidesPerView: 4 }, 1024: { slidesPerView: 5 }, 1200: { slidesPerView: 6 } },
        });
    }

    // Auto-dismiss toasts
    document.querySelectorAll(".toast").forEach(function (t) {
        setTimeout(function () { t.remove(); }, 3500);
    });

    // Size selection
    document.querySelectorAll(".size-box").forEach(function (box) {
        box.addEventListener("click", function () {
            const group = box.closest(".size-row");
            group.querySelectorAll(".size-box").forEach(function (b) { b.classList.remove("selected"); });
            box.classList.add("selected");
            const input = group.querySelector('input[name="size"]');
            if (input) input.value = box.dataset.size;
        });
    });

    // Gallery thumbnails
    document.querySelectorAll(".gallery .thumbs img").forEach(function (thumb) {
        thumb.addEventListener("click", function () {
            const main = document.querySelector(".gallery .main-img img");
            if (main) main.src = thumb.src;
            document.querySelectorAll(".gallery .thumbs img").forEach(function (t) { t.classList.remove("active"); });
            thumb.classList.add("active");
        });
    });

    // Quantity steppers
    document.querySelectorAll(".qty .inc").forEach(function (btn) {
        btn.addEventListener("click", function () {
            const input = btn.parentElement.querySelector("input");
            input.value = parseInt(input.value, 10) + 1;
            input.closest("form").submit();
        });
    });
    document.querySelectorAll(".qty .dec").forEach(function (btn) {
        btn.addEventListener("click", function () {
            const input = btn.parentElement.querySelector("input");
            if (parseInt(input.value, 10) > 1) {
                input.value = parseInt(input.value, 10) - 1;
                input.closest("form").submit();
            }
        });
    });

    // Wishlist toggle via fetch
    function getCookie(name) {
        const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
        return match ? match[2] : "";
    }
    document.querySelectorAll(".wishlist-btn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            const productId = btn.dataset.product;
            const csrf = document.querySelector('meta[name="csrf-token"]').content;
            const url = btn.classList.contains("active") ? "/wishlist/remove/" : "/wishlist/add/";
            const form = new URLSearchParams();
            form.append("product_id", productId);
            form.append("next", window.location.pathname);
            fetch(url, {
                method: "POST",
                headers: { "X-CSRFToken": csrf, "Content-Type": "application/x-www-form-urlencoded" },
                body: form.toString(),
            }).then(function (res) {
                if (res.ok) {
                    btn.classList.toggle("active");
                    const badge = document.querySelector('.action[href="/wishlist/"] .badge');
                    if (badge) {
                        let n = parseInt(badge.textContent, 10) + (btn.classList.contains("active") ? 1 : -1);
                        if (n <= 0) { badge.remove(); } else { badge.textContent = n; }
                    }
                }
            });
        });
    });
});

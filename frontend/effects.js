document.addEventListener("click", function (event) {
 
    const button = event.target.closest("button");
 
    if (!button) {
        return;
    }
 
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height) * 1.4;
 
    const bubble = document.createElement("span");
    bubble.className = "ripple-bubble";
    bubble.style.width = `${size}px`;
    bubble.style.height = `${size}px`;
    bubble.style.left = `${event.clientX - rect.left - size / 2}px`;
    bubble.style.top = `${event.clientY - rect.top - size / 2}px`;
 
    button.appendChild(bubble);
 
    bubble.addEventListener("animationend", function () {
        bubble.remove();
    });
});
 
 
/* ---- sticky header gains a stronger shadow once the page scrolls ---- */
(function () {
 
    const header = document.querySelector(".dashboard-header");
 
    if (!header) {
        return;
    }
 
    function updateHeaderState() {
        if (window.scrollY > 6) {
            header.classList.add("is-scrolled");
        } else {
            header.classList.remove("is-scrolled");
        }
    }
 
    updateHeaderState();
    window.addEventListener("scroll", updateHeaderState, { passive: true });
 
})();
 
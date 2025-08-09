// 5 soniyadan keyin messages'larni yo‘qotish
setTimeout(function() {
    $('.message-box').fadeOut('slow');
}, 5000);

// Tema toggle script
document.addEventListener("DOMContentLoaded", function() {
    const body = document.body;
    const toggleBtn = document.getElementById("themeToggle");

    // Saqlangan rejimni yuklash
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark-mode");
        toggleBtn.textContent = "☀️";
    }

    toggleBtn.addEventListener("click", function() {
        body.classList.toggle("dark-mode");
        if (body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
            toggleBtn.textContent = "☀️";
        } else {
            localStorage.setItem("theme", "light");
            toggleBtn.textContent = "🌙";
        }
    });
});
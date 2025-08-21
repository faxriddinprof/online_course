document.addEventListener("DOMContentLoaded", function () {
    const nextBtn = document.querySelector(".btn-primary, .btn-success");
    if (nextBtn) {
        nextBtn.addEventListener("click", function () {
            const moduleId = document.querySelector(".course-title").dataset.moduleId;
            fetch(`/api/module/${moduleId}/complete/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                }
            });
        });
    }
});

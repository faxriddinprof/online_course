document.addEventListener("DOMContentLoaded", function () {
  const nextBtn = document.querySelector(".course-main .mt-4 a.btn");
  if (!nextBtn) return;

  nextBtn.addEventListener("click", async function (e) {
    e.preventDefault();

    const titleEl = document.querySelector(".course-title");
    const moduleId = titleEl ? titleEl.dataset.moduleId : null;
    const csrf = document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    const nextUrl = nextBtn.getAttribute("href");

    // Agar moduleId topilmasa, shunchaki o'tib ketamiz
    if (!moduleId) {
      window.location.href = nextUrl;
      return;
    }

    // Tugmani takror bosilmasligi uchun bloklaymiz
    nextBtn.setAttribute("disabled", "disabled");

    const apiUrl = `/api/module/${moduleId}/complete/`;

    try {
      // 1) sendBeacon bor bo'lsa — eng ishonchli yo'l
      if ("sendBeacon" in navigator) {
        const fd = new FormData();
        // Django CSRF middleware POST body ichidagi `csrfmiddlewaretoken` keyini ham qabul qiladi
        fd.append("csrfmiddlewaretoken", csrf);
        navigator.sendBeacon(apiUrl, fd);
        // darhol keyingi sahifaga o'tamiz
        window.location.href = nextUrl;
        return;
      }

      // 2) Aks holda fetch + await
      await fetch(apiUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrf,
        },
        credentials: "same-origin",
      });

      window.location.href = nextUrl;
    } catch (err) {
      // Xatoda ham foydalanuvchini ushlab qolmaymiz
      window.location.href = nextUrl;
    }
  });
});

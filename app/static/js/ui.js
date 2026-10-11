
 // UI globale: navbar, animazioni e paginazione.
(function () {
  // Serve al CSS per gli elementi .reveal
  document.documentElement.classList.add("js");

  document.addEventListener("DOMContentLoaded", function () {
    // Navbar: aggiunge un'ombra quando la pagina scorre
    var nav = document.querySelector(".site-nav");

    if (nav) {
      var onScroll = function () {
        nav.classList.toggle("scrolled", window.scrollY > 8);
      };

      onScroll();
      window.addEventListener("scroll", onScroll, { passive: true });
    }

    // Animazione "reveal"
    var els = document.querySelectorAll(".reveal");

    if (!("IntersectionObserver" in window)) {
      els.forEach(function (el) {
        el.classList.add("in");
      });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            io.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.12,
        rootMargin: "0px 0px -40px 0px"
      });

      els.forEach(function (el) {
        io.observe(el);
      });
    }

    // Paginazione: aggiorna l'elenco quando cambia
    // il numero di elementi per pagina.
    var form = document.getElementById("perPageForm");
    var select = document.getElementById("per_page");

    if (form && select) {
      select.addEventListener("change", function () {
        form.requestSubmit();
      });
    }
  });
})();
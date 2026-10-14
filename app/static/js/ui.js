// UI globale: navbar, animazioni, paginazione, snackbar, autocomplete dispensa, password e profilo.
(function () {
  // Serve al CSS per gli elementi .reveal
  document.documentElement.classList.add("js");

  // Conferma prima delle azioni distruttive: <form data-conferma="Sei sicuro?">.
  document.addEventListener("submit", function (e) {
    var msg = e.target.getAttribute && e.target.getAttribute("data-conferma");
    if (msg && !window.confirm(msg)) {
      e.preventDefault();
    }
  });

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
    var form = document.getElementById("perPageForm");
    var select = document.getElementById("per_page");

    if (form && select) {
      select.addEventListener("change", function () {
        form.requestSubmit();
      });
    }

    // --- Chiusura manuale immediata al click sulla "x" dei flash ---
    document.addEventListener("click", function (e) {
      if (e.target.classList.contains("mat-snackbar__close")) {
        var snack = e.target.closest(".mat-snackbar");
        if (snack) {
          snack.style.transition = "opacity 0.15s ease, transform 0.15s ease";
          snack.style.opacity = "0";
          snack.style.transform = "scale(0.9)";
          setTimeout(function () {
            snack.remove();
          }, 150);
        }
      }
    });

    // --- Scomparsa automatica dei flash dopo 3 secondi ---
    var snacks = document.querySelectorAll(".mat-snackbar");
    snacks.forEach(function (snack) {
      setTimeout(function () {
        if (!snack.isConnected) return;
        
        snack.style.transition = "opacity 0.4s ease, transform 0.4s ease";
        snack.style.opacity = "0";
        snack.style.transform = "translateY(16px) scale(0.95)";
        setTimeout(function () {
          if (snack.isConnected) {
            snack.remove();
          }
        }, 400);
      }, 3000);
    });

    // --- Autocomplete e tendina interattiva Ingrediente nella Dispensa ---
    var input = document.getElementById("ingrediente_input");
    var hiddenId = document.getElementById("ingrediente_id");
    var listContainer = document.getElementById("autocomplete-list");

    if (input && hiddenId && listContainer) {
      listContainer.style.display = "none";

      var ingredienti = [];
      try {
        ingredienti = JSON.parse(input.getAttribute("data-ingredienti") || "[]");
      } catch (e) {
        ingredienti = [];
      }

      function mostraLista(lista) {
        if (lista.length === 0) {
          listContainer.style.display = "none";
          return;
        }

        var html = "";
        lista.forEach(function (i) {
          html += '<button type="button" class="dropdown-item py-2 px-3" data-id="' + i.id + '" data-nome="' + i.nome + ' (' + i.unita + ')">' + i.nome + ' <small class="text-muted">(' + i.unita + ')</small></button>';
        });

        listContainer.innerHTML = html;
        listContainer.style.display = "block";
      }

      input.addEventListener("focus", function () {
        hiddenId.value = "";
        mostraLista(ingredienti);
      });

      input.addEventListener("input", function () {
        hiddenId.value = ""; 
        var query = this.value.toLowerCase().trim();
        if (!query) {
          mostraLista(ingredienti);
          return;
        }

        var match = ingredienti.filter(function (i) {
          return i.nome.toLowerCase().includes(query);
        });
        mostraLista(match);
      });

      listContainer.addEventListener("click", function (e) {
        var target = e.target.closest("button");
        if (target) {
          input.value = target.getAttribute("data-nome");
          hiddenId.value = target.getAttribute("data-id");
          listContainer.style.display = "none";
        }
      });

      document.addEventListener("click", function (e) {
        if (!input.contains(e.target) && !listContainer.contains(e.target)) {
          listContainer.style.display = "none";
        }
      });
    }

    // --- Gestione Password (Toggle e Meter a segmenti stile Angular) ---
    var passInput = document.getElementById("password");
    var confirmInput = document.getElementById("conferma_password");

    if (passInput) {
      document.querySelectorAll(".toggle-password-visibility").forEach(function (btn) {
        btn.addEventListener("click", function () {
          var inputContainer = this.closest(".input-container");
          var input = inputContainer ? inputContainer.querySelector("input") : null;
          var icon = this.querySelector(".toggle-icon");
          if (input) {
            if (input.type === "password") {
              input.type = "text";
              if (icon) icon.textContent = "👁️‍🗨️";
              this.setAttribute("aria-label", "Nascondi password");
            } else {
              input.type = "password";
              if (icon) icon.textContent = "👁️";
              this.setAttribute("aria-label", "Mostra password");
            }
          }
        });
      });

      passInput.addEventListener("input", function () {
        var val = this.value;
        let strength = 0;

        if (val.length >= 8) strength++;
        if (/\d/.test(val)) strength++;
        if (/[a-z]/.test(val) && /[A-Z]/.test(val)) strength++;
        if (/[^A-Za-z0-9]/.test(val)) strength++;

        for (let i = 0; i < 4; i++) {
          var seg = document.getElementById("segment-" + i);
          if (!seg) continue;
          
          seg.className = "strength-segment";
          if (val && strength > 0) {
            if (i === 0 && strength >= 1) seg.classList.add("weak");
            if (i === 1 && strength >= 2) seg.classList.add("fair");
            if (i === 2 && strength >= 3) seg.classList.add("good");
            if (i === 3 && strength >= 4) seg.classList.add("strong");
          }
        }
      });
    }

    if (confirmInput && passInput) {
      function checkPasswordMatch() {
        var p1 = passInput.value;
        var p2 = confirmInput.value;
        if (!p2) {
          confirmInput.classList.remove("is-valid", "is-invalid");
          return;
        }
        if (p1 === p2) {
          confirmInput.classList.remove("is-invalid");
          confirmInput.classList.add("is-valid");
        } else {
          confirmInput.classList.remove("is-valid");
          confirmInput.classList.add("is-invalid");
        }
      }
      confirmInput.addEventListener("input", checkPasswordMatch);
    }

    // --- Controllo Modifiche Profilo (Disabilita salva se non ci sono variazioni) ---
    var profileUsername = document.getElementById("username");
    var profileEmail = document.getElementById("email");
    var submitBtn = document.getElementById("submit-btn");

    if (profileUsername && profileEmail && submitBtn) {
      var initialUsername = profileUsername.value;
      var initialEmail = profileEmail.value;

      function checkProfileChanges() {
        var currentUsername = profileUsername.value;
        var currentEmail = profileEmail.value;

        if (currentUsername !== initialUsername || currentEmail !== initialEmail) {
          submitBtn.removeAttribute("disabled");
        } else {
          submitBtn.setAttribute("disabled", "true");
        }
      }

      profileUsername.addEventListener("input", checkProfileChanges);
      profileEmail.addEventListener("input", checkProfileChanges);
    }

  });
})();
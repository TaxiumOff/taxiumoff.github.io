/* =============================================================
   PORTFOLIO – MODÈLE VIERGE
   Petites interactions : thème, menu, révélations, filtres, formulaire.
   ============================================================= */

const root = document.documentElement;

/* ---------- 1. Thème clair / sombre ---------- */
const themeToggle = document.querySelector("#theme-toggle");
const savedTheme = localStorage.getItem("portfolio-theme");

if (savedTheme === "light" || savedTheme === "dark") {
  root.dataset.theme = savedTheme;
}

function syncThemeButton() {
  const isLight = root.dataset.theme === "light";
  themeToggle.setAttribute("aria-pressed", String(isLight));
  themeToggle.setAttribute(
    "aria-label",
    isLight ? "Activer le thème sombre" : "Activer le thème clair"
  );
}

syncThemeButton();

themeToggle.addEventListener("click", () => {
  const next = root.dataset.theme === "light" ? "dark" : "light";
  root.dataset.theme = next;
  localStorage.setItem("portfolio-theme", next);
  syncThemeButton();
});

/* ---------- 2. Menu mobile ---------- */
const menuToggle = document.querySelector("#menu-toggle");
const nav = document.querySelector("#navigation");

function closeMenu() {
  nav.classList.remove("is-open");
  menuToggle.setAttribute("aria-expanded", "false");
  menuToggle.setAttribute("aria-label", "Ouvrir le menu");
}

menuToggle.addEventListener("click", () => {
  const open = !nav.classList.contains("is-open");
  nav.classList.toggle("is-open", open);
  menuToggle.setAttribute("aria-expanded", String(open));
  menuToggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
});

nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeMenu();
});

/* ---------- 3. Apparition des éléments au défilement ---------- */
const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -50px 0px" }
  );
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

/* ---------- 4. Filtre des projets ---------- */
const filters = document.querySelectorAll(".filter");
const projects = document.querySelectorAll(".project-card");

filters.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;

    filters.forEach((item) => {
      const active = item === button;
      item.classList.toggle("is-active", active);
      item.setAttribute("aria-pressed", String(active));
    });

    projects.forEach((card) => {
      const visible = filter === "all" || card.dataset.category === filter;
      card.hidden = !visible;

      if (visible) {
        card.classList.remove("is-visible");
        requestAnimationFrame(() => card.classList.add("is-visible"));
      }
    });
  });
});

/* ---------- 5. Formulaire de contact ----------
   Version sans serveur : ouvre l’application e-mail avec le message pré-rempli.
   À remplacer par un service (Formspree, Resend, backend…) si tu veux un vrai envoi.
   ADRESSE À PERSONNALISER ↓ */
const contactEmail = "ton.email@example.com";

const contactForm = document.querySelector("#contact-form");
const formStatus = document.querySelector("#form-status");

contactForm.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = new FormData(contactForm);
  const subject = encodeURIComponent(`[Portfolio] ${data.get("subject") || "Nouveau message"}`);
  const body = encodeURIComponent(
    `${data.get("name")} (${data.get("email")}) :\n\n${data.get("message")}`
  );

  window.location.href = `mailto:${contactEmail}?subject=${subject}&body=${body}`;
  formStatus.textContent = "Ton application e-mail s’ouvre avec le message pré-rempli.";
});

/* ---------- 6. Année dans le pied de page ---------- */
document.querySelector("#year").textContent = new Date().getFullYear();

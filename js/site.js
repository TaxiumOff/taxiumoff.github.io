/* Interactions du site public : thème, menu, filtres, formulaire, admin. */

const root = document.documentElement;

/* Thème */
const themeToggle = document.querySelector("#theme-toggle");
const savedTheme = localStorage.getItem("portfolio-theme");

if (savedTheme === "light" || savedTheme === "dark") {
  root.dataset.theme = savedTheme;
}

function syncThemeButton() {
  if (!themeToggle) return;
  const isLight = root.dataset.theme === "light";
  themeToggle.setAttribute("aria-pressed", String(isLight));
  themeToggle.setAttribute("aria-label", isLight ? "Activer le thème sombre" : "Activer le thème clair");
}

syncThemeButton();

if (themeToggle) {
  themeToggle.addEventListener("click", () => {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    localStorage.setItem("portfolio-theme", next);
    syncThemeButton();
  });
}

/* Menu mobile */
const menuToggle = document.querySelector("#menu-toggle");
const nav = document.querySelector("#navigation");

function closeMenu() {
  if (!nav || !menuToggle) return;
  nav.classList.remove("is-open");
  menuToggle.setAttribute("aria-expanded", "false");
  menuToggle.setAttribute("aria-label", "Ouvrir le menu");
}

if (menuToggle && nav) {
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
}

/* Apparitions */
const revealItems = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window && revealItems.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add("is-visible");
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

/* Filtres : uniquement les projets personnels */
const personalGrid = document.querySelector("#projects-personal-grid");
const personalEmpty = document.querySelector("#projects-empty");
const majorGrid = document.querySelector("#projects-major-grid");
const majorEmpty = document.querySelector("#projects-big-empty");
let activeCategory = "all";
let activeLanguage = "all";

function applyFilters() {
  if (!personalGrid) return;
  let visible = 0;

  personalGrid.querySelectorAll("article").forEach((card) => {
    const categoryOk = activeCategory === "all" || card.dataset.category === activeCategory;
    const languageOk = activeLanguage === "all" || card.dataset.language === activeLanguage;
    const show = categoryOk && languageOk;
    card.hidden = !show;
    if (show) visible += 1;
  });

  if (personalEmpty) personalEmpty.hidden = visible > 0;
}

function bindFilterGroup(selector, key, setActive) {
  const buttons = document.querySelectorAll(selector);
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const value = button.dataset[key];
      buttons.forEach((item) => {
        const isActive = item.dataset[key] === value;
        item.classList.toggle("is-active", isActive);
        item.setAttribute("aria-pressed", String(isActive));
      });
      setActive(value);
      applyFilters();
    });
  });
}

bindFilterGroup("[data-category-filter]", "categoryFilter", (value) => { activeCategory = value; });
bindFilterGroup("[data-language-filter]", "languageFilter", (value) => { activeLanguage = value; });
applyFilters();

if (majorGrid && majorEmpty) {
  majorEmpty.hidden = majorGrid.querySelectorAll("article").length > 0;
}

/* Formulaire de contact : ouvre l'application e-mail. */
const contactForm = document.querySelector("#contact-form");
const formStatus = document.querySelector("#form-status");
const contactEmail = "ilianmaanan.pro@gmail.com";

if (contactForm) {
  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(contactForm);
    const subject = encodeURIComponent(`[Portfolio] ${data.get("subject") || "Nouveau message"}`);
    const body = encodeURIComponent(`${data.get("name")} (${data.get("email")}) :\n\n${data.get("message")}`);
    window.location.href = `mailto:${contactEmail}?subject=${subject}&body=${body}`;
    if (formStatus) formStatus.textContent = "Votre application e-mail s’ouvre avec le message pré-rempli.";
  });
}

/* Année du pied de page */
const year = document.querySelector("#year");
if (year) year.textContent = new Date().getFullYear();


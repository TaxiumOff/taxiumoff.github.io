/* =============================================================
   PORTFOLIO – MODÈLE VIERGE
   Petites interactions : thème, menu, révélations, filtres, lecteur de code, formulaire.
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

/* ---------- 4. Filtres des projets personnels ----------
   Catégories : jeux-video | cybersecurite
   Langages  : python | cpp
   Les projets majeurs sont présentés à part, sans filtre. */
const categoryFilters = document.querySelectorAll("[data-category-filter]");
const languageFilters = document.querySelectorAll("[data-language-filter]");
const smallGrid = document.querySelector("#projects-personal-grid");
const smallEmpty = document.querySelector("#projects-empty");
const bigGrid = document.querySelector("#projects-major-grid");
const bigEmpty = document.querySelector("#projects-big-empty");

let activeCategory = "all";
let activeLanguage = "all";

/* Les projets personnels se filtrent par catégorie ET langage. */
function applyProjectFilters() {
  if (!smallGrid) return;

  let visibleCount = 0;

  smallGrid.querySelectorAll(".project-card").forEach((card) => {
    const categoryOk = activeCategory === "all" || card.dataset.category === activeCategory;
    const languageOk = activeLanguage === "all" || card.dataset.language === activeLanguage;
    const visible = categoryOk && languageOk;

    card.hidden = !visible;

    if (visible) {
      visibleCount += 1;
      card.classList.remove("is-visible");
      requestAnimationFrame(() => card.classList.add("is-visible"));
    }
  });

  if (smallEmpty) smallEmpty.hidden = visibleCount > 0;
}

/* Les projets majeurs ne sont pas filtrés : ils sont toujours tous visibles. */
if (bigGrid && bigEmpty) {
  bigEmpty.hidden = bigGrid.querySelectorAll(".project-showcase, .project-card--big").length > 0;
}

function bindFilterGroup(buttons, key, onSelect) {
  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const value = button.dataset[key];

      buttons.forEach((item) => {
        const active = item.dataset[key] === value;
        item.classList.toggle("is-active", active);
        item.setAttribute("aria-pressed", String(active));
      });

      onSelect(value);
      applyProjectFilters();
    });
  });
}

bindFilterGroup(categoryFilters, "categoryFilter", (value) => { activeCategory = value; });
bindFilterGroup(languageFilters, "languageFilter", (value) => { activeLanguage = value; });
applyProjectFilters();

/* ---------- 5. Lecteur de code en lecture seule ----------
   Les fichiers sont chargés depuis source_code/<projet> puis coloriés
   côté navigateur, sans bibliothèque et sans possibilité d'édition. */
const codePatterns = {
  python: /("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|#[^\n]*|\b(?:def|class|return|if|elif|else|for|while|in|not|and|or|import|from|as|with|try|except|finally|raise|lambda|yield|pass|break|continue|global|nonlocal|del|assert|async|await|True|False|None|self)\b|\b\d+(?:\.\d+)?\b)/gm,
  cpp: /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|#[^\n]*|\b(?:include|define|ifndef|ifdef|endif|int|char|float|double|void|bool|auto|const|constexpr|static|extern|return|if|else|for|while|do|switch|case|default|break|continue|class|struct|enum|public|private|protected|namespace|using|template|typename|new|delete|this|true|false|nullptr|std|string|vector)\b|\b\d+(?:\.\d+)?\b)/gm,
  js: /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|`(?:\\.|[^`\\])*`|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\b(?:const|let|var|function|return|if|else|for|while|class|new|async|await|import|from|export|default|true|false|null|undefined)\b|\b\d+(?:\.\d+)?\b)/gm,
  generic: /(\/\/[^\n]*|\/\*[\s\S]*?\*\/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|#[^\n]*|\b\d+(?:\.\d+)?\b)/gm,
};

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function detectCodeLanguage(path) {
  const extension = path.split(".").pop().toLowerCase();
  if (["py", "pyw"].includes(extension)) return "python";
  if (["cpp", "cc", "cxx", "h", "hpp", "hh", "c"].includes(extension)) return "cpp";
  if (["js", "mjs", "cjs", "ts", "tsx", "jsx"].includes(extension)) return "js";
  return "generic";
}

function tokenClass(token, language) {
  if (/^("""|'''|["'`])/.test(token)) return "tok-string";
  if (/^\/\//.test(token) || /^\/\*/.test(token)) return "tok-comment";
  if (/^#/.test(token)) return language === "python" ? "tok-comment" : "tok-preproc";
  if (/^\d/.test(token)) return "tok-number";
  return "tok-keyword";
}

function highlightCode(code, language) {
  const pattern = new RegExp(codePatterns[language].source, "gm");
  let output = "";
  let lastIndex = 0;
  let match;

  while ((match = pattern.exec(code)) !== null) {
    const token = match[0];
    output += escapeHtml(code.slice(lastIndex, match.index));
    output += `<span class="${tokenClass(token, language)}">${escapeHtml(token)}</span>`;
    lastIndex = match.index + token.length;
  }

  return output + escapeHtml(code.slice(lastIndex));
}

async function loadCodeBlocks() {
  const codeBlocks = document.querySelectorAll("[data-code-src]");
  if (!codeBlocks.length) return;

  if (window.location.protocol === "file:") {
    codeBlocks.forEach((block) => {
      block.textContent = "Lance le site avec python -m http.server 8000 pour afficher le code.";
    });
    return;
  }

  for (const block of codeBlocks) {
    const path = block.dataset.codeSrc;
    try {
      const response = await fetch(path);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const code = (await response.text()).replace(/\r\n?/g, "\n");
      block.innerHTML = highlightCode(code, detectCodeLanguage(path));

      const editor = block.closest(".code-editor");
      const gutter = editor && editor.querySelector(".code-editor__gutter");
      if (gutter) {
        const lines = code.replace(/\n$/, "").split("\n").length;
        gutter.textContent = Array.from({ length: lines }, (_, i) => i + 1).join("\n");
      }
    } catch {
      block.textContent = `Code introuvable : ${path}`;
    }
  }
}

async function loadCodeReports() {
  const reports = document.querySelectorAll("[data-report-src]");
  if (!reports.length || window.location.protocol === "file:") return;

  for (const report of reports) {
    try {
      const response = await fetch(report.dataset.reportSrc);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      report.textContent = await response.text();
    } catch {
      report.textContent = "Rapport introuvable.";
    }
  }
}

loadCodeBlocks();
loadCodeReports();

/* ---------- 6. Formulaire de contact ----------
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
  formStatus.textContent = "Votre application e-mail s’ouvre avec le message pré-rempli.";
});

/* ---------- 7. Année dans le pied de page ---------- */
document.querySelector("#year").textContent = new Date().getFullYear();

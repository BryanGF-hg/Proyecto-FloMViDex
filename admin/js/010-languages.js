  // ============================================
  // 11. TRADUCCIONES
  // ============================================
  let translations = {};
  let currentLang = localStorage.getItem('flomvidex_lang') || 'es';
  
  async function loadTranslations() {
    const res = await fetch('css/traducciones.json');
    translations = await res.json();
  }
  
  function t(key, vars = {}) {
    let text = translations[currentLang]?.[key] || key;
    for (const k in vars) {
      text = text.replace(`{${k}}`, vars[k]);
    }
    return text;
  }
  
  function applyTranslations() {
    document.title = t("title");
    document.querySelector("header h1").textContent = t("title");
    
    const h3 = document.querySelector("#current-directory-label h3");
    h3.textContent = t("current_dir");
    
    searchInput.placeholder = t("search_placeholder");
    
    const opts = extensionFilter.querySelectorAll("option");
    opts[0].textContent = t("all_extensions");
    opts[1].textContent = t("only_opus");
    opts[2].textContent = t("only_mp3");
    
    deleteSelectedBtn.textContent = t("delete_selected");
    exportJsonBtn.textContent    = t("export_json");
    
    const h2s = document.querySelectorAll("header h2");
    h2s[0].textContent = t("player_title");
    h2s[1].textContent = t("create_title");
    
    document.querySelector("input[name=title]").placeholder  = t("title_placeholder");
    document.querySelector("input[name=artist]").placeholder = t("artist_placeholder");
    document.querySelector("input[name=tags]").placeholder   = t("tags_placeholder");
    document.querySelector("#create-form button").textContent = t("upload_btn");
    
    document.getElementById("lang-toggle").textContent = currentLang === "es" ? "EN" : "ES";
  }

  const langToggle = document.getElementById('lang-toggle');
  langToggle.addEventListener("click", () => {
    currentLang = currentLang === "es" ? "en" : "es";
    localStorage.setItem("flomvidex_lang", currentLang);
    applyTranslations();
    loadTracks();
  });

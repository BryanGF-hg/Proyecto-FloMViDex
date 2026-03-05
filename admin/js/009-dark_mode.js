  // ============================================
  // 10. MODO OSCURO
  // ============================================
  const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;
  
  const savedTheme = localStorage.getItem('flomvidex_theme');
  if (savedTheme === 'dark') {
    body.classList.add('dark-mode');
    themeToggle.textContent = '☀️';
  }

  themeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
      themeToggle.textContent = '☀️';
      localStorage.setItem('flomvidex_theme', 'dark');
    } else {
      themeToggle.textContent = '🌙';
      localStorage.setItem('flomvidex_theme', 'light');
    }
  });

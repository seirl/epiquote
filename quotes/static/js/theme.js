(function() {
  const getStoredTheme = () => localStorage.getItem('theme');
  const setStoredTheme = theme => {
    localStorage.setItem('theme', theme);
    setTheme(theme);
  };
  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  };

  const setTheme = theme => {
    document.documentElement.setAttribute('data-bs-theme', theme);
  };

  setTheme(getPreferredTheme());

  window.toggleTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setStoredTheme(newTheme);
  };

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (!getStoredTheme()) {
      setTheme(getPreferredTheme());
    }
  });
})();

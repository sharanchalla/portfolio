// Immediately invoked to prevent theme flashing on load
(function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
    } else {
        const systemPrefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
        document.documentElement.setAttribute('data-theme', systemPrefersLight ? 'light' : 'dark');
    }
})();

// Function called by the theme toggle button
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Immediately invoked to prevent theme flashing and ensure live local server connection
(function() {
    // If opened directly from Windows Explorer (file:// protocol), automatically redirect to the running local Flask server
    if (window.location.protocol === 'file:') {
        try {
            let filename = window.location.pathname.split(/[\\\/]/).pop().replace('.html', '').toLowerCase();
            let targetRoute = (filename === 'index' || filename === '') ? '' : filename;
            window.location.replace('http://127.0.0.1:5000/' + targetRoute);
            return;
        } catch (e) {
            console.warn('Redirect to local server failed:', e);
        }
    }

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

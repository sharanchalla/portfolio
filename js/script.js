document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('open');
        });
    }

    // Close menu when clicking a link on mobile
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu) navMenu.classList.remove('open');
        });
    });

    // 2. Active Page Highlight
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        // Handle root / home paths matching active nav-links
        if (currentPath === href || 
            (currentPath === '/' && href === '/') || 
            (currentPath === '/home' && href === '/')) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });

    // 3. Skill Bars Animation on Scroll
    const skillBars = document.querySelectorAll('.skill-bar');
    if (skillBars.length > 0) {
        const animateSkills = () => {
            skillBars.forEach(bar => {
                const rect = bar.getBoundingClientRect();
                const viewHeight = Math.max(document.documentElement.clientHeight, window.innerHeight);
                // Check if progress bar is inside viewport
                if (rect.top <= viewHeight && rect.bottom >= 0) {
                    const progress = bar.getAttribute('data-progress');
                    bar.style.width = `${progress}%`;
                }
            });
        };
        // Call immediately and bind to scroll listener
        animateSkills();
        window.addEventListener('scroll', animateSkills);
    }

    // 4. AJAX Contact Form Submission
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            submitBtn.innerHTML = 'Sending...';
            submitBtn.disabled = true;
            
            const formData = new FormData(contactForm);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });
            
            try {
                const response = await fetch('/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok && result.success) {
                    showToast(result.message || 'Message sent!', 'success');
                    contactForm.reset();
                } else {
                    showToast(result.message || 'Failed to send message.', 'error');
                }
            } catch (error) {
                console.error('Error submitting contact form:', error);
                showToast('A network error occurred. Please try again.', 'error');
            } finally {
                submitBtn.innerHTML = originalBtnText;
                submitBtn.disabled = false;
            }
        });
    }

    // 5. Custom Toast Notifications
    function showToast(message, type = 'success') {
        let toast = document.getElementById('toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'toast';
            toast.className = 'toast';
            document.body.appendChild(toast);
        }
        
        toast.className = `toast toast-${type} show`;
        toast.innerHTML = `
            <div class="toast-content">
                <span>${message}</span>
            </div>
        `;
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 4000);
    }
});

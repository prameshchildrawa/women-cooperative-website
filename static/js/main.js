/**
 * Main JavaScript for Women Community Multipurpose Cooperative Ltd.
 */

(function() {
    'use strict';

    // ===== Dark Mode Toggle =====
    const darkModeToggle = document.getElementById('darkModeToggle');
    const html = document.documentElement;

    // Check for saved dark mode preference or default to 'light'
    const getDarkModePreference = () => {
        const savedMode = localStorage.getItem('darkMode');
        if (savedMode) {
            return savedMode === 'dark';
        }
        // Check system preference
        return window.matchMedia('(prefers-color-scheme: dark)').matches;
    };

    // Apply dark mode
    const applyDarkMode = (isDark) => {
        if (isDark) {
            html.setAttribute('data-bs-theme', 'dark');
            darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            localStorage.setItem('darkMode', 'dark');
        } else {
            html.setAttribute('data-bs-theme', 'light');
            darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            localStorage.setItem('darkMode', 'light');
        }
    };

    // Initialize dark mode
    if (darkModeToggle) {
        applyDarkMode(getDarkModePreference());

        darkModeToggle.addEventListener('click', () => {
            const isDark = html.getAttribute('data-bs-theme') === 'dark';
            applyDarkMode(!isDark);
        });
    }

    // ===== Popup Notice =====
    const showPopupNotice = () => {
        const popupModal = document.getElementById('noticePopupModal');
        if (!popupModal) return;

        const popupId = popupModal.dataset.noticeId || 'default';
        const storageKey = `popupShown_${popupId}`;
        const lastShown = localStorage.getItem(storageKey);
        const delayDays = parseInt(popupModal.dataset.delay) || 7;
        const delayMs = delayDays * 24 * 60 * 60 * 1000;

        const shouldShow = !lastShown || (Date.now() - parseInt(lastShown) > delayMs);

        if (shouldShow) {
            const modal = new bootstrap.Modal(popupModal);
            modal.show();
            localStorage.setItem(storageKey, Date.now().toString());
        }
    };

    // Show popup after page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', showPopupNotice);
    } else {
        showPopupNotice();
    }

    // ===== Newsletter Form =====
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(newsletterForm);
            const submitBtn = newsletterForm.querySelector('button[type="submit"]');
            const originalContent = submitBtn.innerHTML;

            try {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

                const response = await fetch(newsletterForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });

                const data = await response.json();

                if (data.success) {
                    showAlert('success', data.message);
                    newsletterForm.reset();
                } else {
                    showAlert('warning', data.message);
                }
            } catch (error) {
                showAlert('danger', 'An error occurred. Please try again.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalContent;
            }
        });
    }

    // ===== Alert Helper =====
    const showAlert = (type, message) => {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alertDiv);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    };

    // ===== Smooth Scroll =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ===== Navbar Scroll Effect =====
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('shadow');
            } else {
                navbar.classList.remove('shadow');
            }
        });
    }

    // ===== Form Validation Enhancement =====
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // ===== Lazy Loading Images =====
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ===== Search Form Focus =====
    const searchInput = document.querySelector('input[type="search"]');
    if (searchInput) {
        searchInput.addEventListener('focus', () => {
            searchInput.parentElement.classList.add('shadow-sm');
        });
        searchInput.addEventListener('blur', () => {
            searchInput.parentElement.classList.remove('shadow-sm');
        });
    }

    // ===== Hero Slider Animation Reset =====
    const heroCarousel = document.getElementById('heroCarousel');
    if (heroCarousel) {
        heroCarousel.addEventListener('slide.bs.carousel', () => {
            const activeSlide = heroCarousel.querySelector('.carousel-item.active');
            const animatedElements = activeSlide.querySelectorAll('.animate-fade-in, .animate-fade-in-delay, .animate-fade-in-delay-2');
            animatedElements.forEach(el => {
                el.style.animation = 'none';
                el.offsetHeight; // Trigger reflow
                el.style.animation = null;
            });
        });
    }

    // ===== Counter Animation =====
    const animateCounters = () => {
        const counters = document.querySelectorAll('.counter');
        counters.forEach(counter => {
            const target = parseInt(counter.dataset.target);
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += step;
                if (current < target) {
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        updateCounter();
                        observer.unobserve(counter);
                    }
                });
            });

            observer.observe(counter);
        });
    };

    // Initialize counters
    animateCounters();

    // ===== Back to Top Button =====
    const createBackToTopButton = () => {
        const button = document.createElement('button');
        button.innerHTML = '<i class="fas fa-arrow-up"></i>';
        button.className = 'btn btn-success position-fixed bottom-0 end-0 m-4 rounded-circle shadow';
        button.style.cssText = 'width: 50px; height: 50px; display: none; z-index: 999;';
        button.setAttribute('aria-label', 'Back to top');
        document.body.appendChild(button);

        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        });

        button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    };

    createBackToTopButton();

    // ===== Print Functionality =====
    window.printPage = () => {
        window.print();
    };

    // ===== Share Functionality =====
    window.sharePage = (platform) => {
        const url = encodeURIComponent(window.location.href);
        const title = encodeURIComponent(document.title);
        let shareUrl = '';

        switch(platform) {
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                break;
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
                break;
            case 'linkedin':
                shareUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`;
                break;
            case 'whatsapp':
                shareUrl = `https://wa.me/?text=${title}%20${url}`;
                break;
        }

        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    };

    // ===== Accessibility Enhancements =====
    // Skip to main content
    const mainContent = document.querySelector('main');
    if (mainContent && !document.getElementById('skip-link')) {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.id = 'skip-link';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'position-absolute visually-hidden-focusable bg-primary text-white p-2';
        skipLink.style.cssText = 'top: 0; left: 0; z-index: 10000;';
        mainContent.id = 'main-content';
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    // ===== Initialize Tooltips =====
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ===== Initialize Popovers =====
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    console.log('✅ MSMC Website JS Loaded');
})();

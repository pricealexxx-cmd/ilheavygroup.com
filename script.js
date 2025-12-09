// Mobile Navigation Toggle
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav-menu');

if (burger) {
    burger.addEventListener('click', () => {
        nav.classList.toggle('active');
        burger.classList.toggle('active');
    });
}

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (nav && burger && !nav.contains(e.target) && !burger.contains(e.target)) {
        nav.classList.remove('active');
        burger.classList.remove('active');
    }
});

// Auto-select product from URL parameter
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const productParam = urlParams.get('product');
    const productSelect = document.getElementById('product');
    
    if (productParam && productSelect) {
        productSelect.value = productParam;
        // Scroll to form
        productSelect.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});

// EmailJS Configuration
const EMAILJS_PUBLIC_KEY = 'XZm-z0qbBAHBbiduM';
const EMAILJS_SERVICE_ID = 'service_8bd4u9h';
const EMAILJS_TEMPLATE_ID = 'template_kgedaps';

// Initialize EmailJS
function initEmailJS() {
    if (typeof emailjs !== 'undefined') {
        emailjs.init(EMAILJS_PUBLIC_KEY);
    } else {
        // Retry if EmailJS hasn't loaded yet
        setTimeout(initEmailJS, 100);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initEmailJS);

// Form Submission Handler with EmailJS
const contactForm = document.getElementById('contactForm');

if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Disable submit button to prevent double submission
        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.textContent = 'Sending...';
        
        const formData = {
            name: document.getElementById('name').value,
            company: document.getElementById('company').value || 'Not provided',
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            message: document.getElementById('message').value,
            product: document.getElementById('product') ? document.getElementById('product').value : 'General Inquiry'
        };

        // Prepare template parameters for EmailJS
        const templateParams = {
            from_name: formData.name,
            from_email: formData.email,
            from_phone: formData.phone,
            company: formData.company,
            product_interest: formData.product,
            message: formData.message,
            to_email: 'info@ilheavygroup.com'
        };

        try {
            // Check if EmailJS is initialized
            if (typeof emailjs === 'undefined') {
                throw new Error('EmailJS is not loaded. Please check your configuration.');
            }
            
            // Check if configuration is set
            if (EMAILJS_SERVICE_ID === 'YOUR_SERVICE_ID' || EMAILJS_TEMPLATE_ID === 'YOUR_TEMPLATE_ID' || EMAILJS_PUBLIC_KEY === 'YOUR_PUBLIC_KEY') {
                throw new Error('EmailJS is not configured. Please set your Service ID, Template ID, and Public Key in script.js');
            }
            
            // Send email using EmailJS
            await emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, templateParams);
            
            // Show success message
            showNotification('Thank you! Your message has been sent. We will contact you shortly.', 'success');
            
            // Reset form
            contactForm.reset();
            
        } catch (error) {
            console.error('EmailJS Error:', error);
            let errorMessage = 'Sorry, there was an error sending your message. ';
            if (error.text) {
                errorMessage += error.text;
            } else if (error.message) {
                errorMessage += error.message;
            } else {
                errorMessage += 'Please try again or contact us directly.';
            }
            showNotification(errorMessage, 'error');
        } finally {
            // Re-enable submit button
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
}

// Notification Function
function showNotification(message, type = 'success') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 10000;
        animation: slideIn 0.3s ease-out;
    `;

    // Add to page
    document.body.appendChild(notification);

    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Add active class to current page in navigation
const currentLocation = location.pathname.split('/').pop() || 'index.html';
document.querySelectorAll('.nav-menu a').forEach(link => {
    if (link.getAttribute('href') === currentLocation) {
        link.classList.add('active');
    }
});

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\d\s\-\+\(\)]+$/;
    return re.test(phone) && phone.replace(/\D/g, '').length >= 10;
}

// Add real-time validation to form fields
if (contactForm) {
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');

    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            if (this.value && !validateEmail(this.value)) {
                this.style.borderColor = '#dc3545';
                showNotification('Please enter a valid email address', 'error');
            } else {
                this.style.borderColor = '';
            }
        });
    }

    if (phoneInput) {
        phoneInput.addEventListener('blur', function() {
            if (this.value && !validatePhone(this.value)) {
                this.style.borderColor = '#dc3545';
                showNotification('Please enter a valid phone number', 'error');
            } else {
                this.style.borderColor = '';
            }
        });
    }
}

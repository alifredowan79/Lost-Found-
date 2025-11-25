// Dynamic Login Page JavaScript - Updated for Flask Backend

// Global variables
let isPasswordVisible = false;
let loginAttempts = 0;
const maxLoginAttempts = 3;

// Initialize login page
document.addEventListener('DOMContentLoaded', function() {
    initializeLoginPage();
    setupEventListeners();
    checkRememberedUser();
    addFormAnimations();
});

// Initialize login page
function initializeLoginPage() {
    // Add entrance animations
    const formContainer = document.querySelector('.login-form-container');
    const infoPanel = document.querySelector('.login-info-panel');
    
    setTimeout(() => {
        if (formContainer) formContainer.classList.add('fade-in');
    }, 200);
    
    setTimeout(() => {
        if (infoPanel) infoPanel.classList.add('fade-in');
    }, 400);
    
    // Initialize form validation
    setupFormValidation();
    
    // Add floating animation to shapes
    animateFloatingShapes();
}

// Setup event listeners
function setupEventListeners() {
    // Password toggle
    const passwordToggle = document.getElementById('passwordToggle');
    if (passwordToggle) {
        passwordToggle.addEventListener('click', togglePasswordVisibility);
    }
    
    // Forgot password
    const forgotPasswordLink = document.getElementById('forgotPassword');
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', openForgotPasswordModal);
    }
    
    // Sign up link
    const signUpLink = document.getElementById('signUpLink');
    if (signUpLink) {
        signUpLink.addEventListener('click', openSignUpModal);
    }
    
    // Modal close buttons
    const closeForgotModal = document.getElementById('closeForgotModal');
    const closeSignUpModal = document.getElementById('closeSignUpModal');
    
    if (closeForgotModal) closeForgotModal.addEventListener('click', closeModal);
    if (closeSignUpModal) closeSignUpModal.addEventListener('click', closeModal);
    
    // Modal background clicks
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
    });
    
    // Forgot password form
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', handleForgotPassword);
    }
    
    // Sign up form
    const signUpForm = document.getElementById('signUpForm');
    if (signUpForm) {
        signUpForm.addEventListener('submit', handleSignUp);
    }
    
    // Social login buttons
    const socialButtons = document.querySelectorAll('.social-btn');
    socialButtons.forEach(button => {
        button.addEventListener('click', handleSocialLogin);
    });
    
    // Input focus effects
    setupInputFocusEffects();
    
    // Form validation on input
    setupRealTimeValidation();
}

// Toggle password visibility
function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('#passwordToggle i');
    
    if (!passwordInput || !toggleIcon) return;
    
    isPasswordVisible = !isPasswordVisible;
    
    if (isPasswordVisible) {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

// Show field error
function showFieldError(fieldName, message) {
    const field = document.getElementById(fieldName);
    const errorElement = document.getElementById(fieldName + 'Error');
    
    if (field && errorElement) {
        field.classList.add('error');
        errorElement.textContent = message;
        errorElement.classList.add('show');
        
        // Add shake animation
        field.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            field.style.animation = '';
        }, 500);
    }
}

// Clear all errors
function clearAllErrors() {
    const errorElements = document.querySelectorAll('.error-message');
    const inputFields = document.querySelectorAll('.input-container input');
    
    errorElements.forEach(error => {
        error.classList.remove('show');
        error.textContent = '';
    });
    
    inputFields.forEach(field => {
        field.classList.remove('error');
    });
}

// Open forgot password modal
function openForgotPasswordModal(e) {
    e.preventDefault();
    const modal = document.getElementById('forgotPasswordModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

// Open sign up modal
function openSignUpModal(e) {
    e.preventDefault();
    const modal = document.getElementById('signUpModal');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

// Close modal
function closeModal() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.classList.remove('active');
    });
    document.body.style.overflow = '';
}

// Handle forgot password
function handleForgotPassword(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const email = formData.get('resetEmail');
    
    if (!isValidEmail(email)) {
        showFieldError('resetEmail', 'Please enter a valid email address');
        return;
    }
    
    // Show loading state
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;
    
    // Simulate sending reset email
    setTimeout(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        
        // Show success message
        alert('Password reset link has been sent to your email address.');
        closeModal();
        e.target.reset();
    }, 2000);
}

// Handle sign up
function handleSignUp(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const firstName = formData.get('firstName');
    const lastName = formData.get('lastName');
    const email = formData.get('signupEmail');
    const password = formData.get('signupPassword');
    const confirmPassword = formData.get('confirmPassword');
    const agreeTerms = formData.get('agreeTerms');
    
    // Clear previous errors
    clearAllErrors();
    
    // Validate form
    if (!validateSignUpForm(firstName, lastName, email, password, confirmPassword, agreeTerms)) {
        return;
    }
    
    // Show loading state
    const submitBtn = e.target.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Creating Account...';
    submitBtn.disabled = true;
    
    // Simulate account creation
    setTimeout(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
        
        // Show success message
        alert('Account created successfully! You can now log in.');
        closeModal();
        e.target.reset();
    }, 2000);
}

// Validate sign up form
function validateSignUpForm(firstName, lastName, email, password, confirmPassword, agreeTerms) {
    let isValid = true;
    
    if (!firstName || firstName.trim() === '') {
        showFieldError('firstName', 'First name is required');
        isValid = false;
    }
    
    if (!lastName || lastName.trim() === '') {
        showFieldError('lastName', 'Last name is required');
        isValid = false;
    }
    
    if (!email || !isValidEmail(email)) {
        showFieldError('signupEmail', 'Please enter a valid email address');
        isValid = false;
    }
    
    if (!password || password.length < 8) {
        showFieldError('signupPassword', 'Password must be at least 8 characters');
        isValid = false;
    }
    
    if (password !== confirmPassword) {
        showFieldError('confirmPassword', 'Passwords do not match');
        isValid = false;
    }
    
    if (!agreeTerms) {
        alert('Please agree to the Terms of Service and Privacy Policy');
        isValid = false;
    }
    
    return isValid;
}

// Handle social login
function handleSocialLogin(e) {
    const provider = e.target.classList.contains('google-btn') ? 'Google' : 'Microsoft';
    
    // Show loading state
    const originalText = e.target.textContent;
    e.target.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting...';
    e.target.disabled = true;
    
    // Simulate social login
    setTimeout(() => {
        e.target.textContent = originalText;
        e.target.disabled = false;
        
        // For demo purposes, redirect to dashboard
        window.location.href = '/dashboard';
    }, 2000);
}

// Setup form validation
function setupFormValidation() {
    const inputs = document.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                validateField(this);
            }
        });
    });
}

// Validate individual field
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';
    
    if (!value) {
        isValid = false;
        errorMessage = 'This field is required';
    } else {
        switch (fieldName) {
            case 'username':
                if (!isValidEmail(value) && value.length < 3) {
                    isValid = false;
                    errorMessage = 'Please enter a valid username or email';
                }
                break;
            case 'password':
            case 'signupPassword':
                if (value.length < 6) {
                    isValid = false;
                    errorMessage = 'Password must be at least 6 characters';
                }
                break;
            case 'signupEmail':
            case 'resetEmail':
                if (!isValidEmail(value)) {
                    isValid = false;
                    errorMessage = 'Please enter a valid email address';
                }
                break;
            case 'confirmPassword':
                const password = document.getElementById('signupPassword').value;
                if (value !== password) {
                    isValid = false;
                    errorMessage = 'Passwords do not match';
                }
                break;
        }
    }
    
    if (isValid) {
        clearFieldError(field);
    } else {
        showFieldError(field.id, errorMessage);
    }
    
    return isValid;
}

// Clear field error
function clearFieldError(field) {
    const errorElement = document.getElementById(field.id + 'Error');
    if (errorElement) {
        errorElement.classList.remove('show');
        errorElement.textContent = '';
    }
    field.classList.remove('error');
}

// Setup real-time validation
function setupRealTimeValidation() {
    const inputs = document.querySelectorAll('input');
    
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value.trim() !== '') {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
    });
}

// Setup input focus effects
function setupInputFocusEffects() {
    const inputs = document.querySelectorAll('.input-container input');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

// Check remembered user
function checkRememberedUser() {
    // This functionality is now handled by Flask sessions
    // Keeping for compatibility
}

// Add form animations
function addFormAnimations() {
    const formGroups = document.querySelectorAll('.form-group');
    
    formGroups.forEach((group, index) => {
        group.style.animationDelay = `${index * 0.1}s`;
        group.classList.add('slide-up');
    });
}

// Animate floating shapes
function animateFloatingShapes() {
    const shapes = document.querySelectorAll('.shape');
    
    shapes.forEach((shape, index) => {
        const delay = index * 0.5;
        const duration = 6 + (index * 0.5);
        
        shape.style.animationDelay = `${delay}s`;
        shape.style.animationDuration = `${duration}s`;
    });
}

// Utility functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Add shake animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .input-container.focused .input-icon {
        color: #667eea;
    }
    
    .input-container input.has-value + label {
        top: -0.5rem;
        left: 0.75rem;
        font-size: 0.8rem;
        color: #667eea;
        background: #ffffff;
        padding: 0 0.5rem;
    }
`;
document.head.appendChild(style);

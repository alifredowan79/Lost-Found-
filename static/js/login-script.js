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
    
    // Sign up form - use event delegation in case modal is loaded dynamically
    document.addEventListener('submit', function(e) {
        if (e.target && e.target.id === 'signUpForm') {
            console.log('Sign up form submitted via event delegation');
            handleSignUp(e);
        }
    });
    
    // Also attach directly if form exists
    const signUpForm = document.getElementById('signUpForm');
    if (signUpForm) {
        console.log('Sign up form found, attaching direct event listener...');
        signUpForm.addEventListener('submit', handleSignUp);
        console.log('Sign up form event listener attached');
    } else {
        console.warn('Sign up form not found initially (will use event delegation)');
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
    let errorElement = document.getElementById(fieldName + 'Error');
    
    if (field) {
        field.classList.add('error');
        
        // Create error element if it doesn't exist
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = fieldName + 'Error';
            errorElement.className = 'error-message';
            // Insert after the input container
            const inputContainer = field.closest('.input-container') || field.parentElement;
            if (inputContainer) {
                inputContainer.appendChild(errorElement);
            } else {
                field.parentElement.insertAdjacentElement('afterend', errorElement);
            }
        }
        
        errorElement.textContent = message;
        errorElement.classList.add('show');
        
        // Add shake animation
        field.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            field.style.animation = '';
        }, 500);
    } else {
        // If field not found, show alert
        console.error(`Field ${fieldName} not found`);
        alert(message);
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
        
        // Ensure form has event listener when modal opens
        const signUpForm = document.getElementById('signUpForm');
        if (signUpForm) {
            // Remove existing listeners to avoid duplicates
            const newForm = signUpForm.cloneNode(true);
            signUpForm.parentNode.replaceChild(newForm, signUpForm);
            // Re-attach listener
            newForm.addEventListener('submit', handleSignUp);
            console.log('Sign up form event listener re-attached when modal opened');
        }
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
    console.log('Sign up form submitted!');
    
    const formData = new FormData(e.target);
    const firstName = formData.get('firstName');
    const lastName = formData.get('lastName');
    const email = formData.get('signupEmail');
    const password = formData.get('signupPassword');
    const confirmPassword = formData.get('confirmPassword');
    const agreeTerms = formData.get('agreeTerms');
    
    console.log('Form data:', { firstName, lastName, email, password: password ? '***' : '', agreeTerms });
    
    // Clear previous errors
    clearAllErrors();
    
    // Validate form
    if (!validateSignUpForm(firstName, lastName, email, password, confirmPassword, agreeTerms)) {
        console.log('Validation failed');
        return;
    }
    
    console.log('Validation passed, proceeding with registration...');
    
    // Generate username from email if not provided
    let username = email.split('@')[0] || '';
    
    // If username is too short, use first name + last name
    if (username.length < 3) {
        username = (firstName + lastName).toLowerCase().replace(/\s+/g, '');
    }
    
    // If still too short, add numbers
    if (username.length < 3) {
        username = username + '123';
    }
    
    // Ensure username is at least 3 characters
    username = username.substring(0, 20); // Limit to 20 chars
    
    console.log('Registration data:', { username, email, password: '***' });
    
    // Create form data for backend
    const registrationData = new FormData();
    registrationData.append('username', username);
    registrationData.append('email', email);
    registrationData.append('password', password);
    registrationData.append('confirmPassword', confirmPassword);
    registrationData.append('firstName', firstName || '');
    registrationData.append('lastName', lastName || '');
    
    // Show loading state
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (!submitBtn) {
        console.error('Submit button not found!');
        alert('Error: Submit button not found. Please refresh the page.');
        return;
    }
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating Account...';
    submitBtn.disabled = true;
    
    // Submit to backend
    console.log('Submitting registration to /register...');
    fetch('/register', {
        method: 'POST',
        body: registrationData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers.get('content-type'));
        
        // Check if response is JSON
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json().then(data => {
                console.log('Response data:', data);
                return data;
            });
        } else {
            // If not JSON, read as text to see what happened
            return response.text().then(text => {
                console.error('Non-JSON response:', text.substring(0, 200));
                throw new Error('Server returned non-JSON response. Please check the console for details.');
            });
        }
    })
    .then(data => {
        if (data.success) {
            console.log('Registration successful!');
            alert(data.message || 'Account created successfully! You can now log in.');
            closeModal();
            e.target.reset();
            // Optionally redirect to login
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            console.error('Registration failed:', data.message);
            alert(data.message || 'Registration failed. Please try again.');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        }
    })
    .catch(error => {
        console.error('Registration error:', error);
        alert('An error occurred: ' + (error.message || 'Please try again. Check the browser console for details.'));
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// Validate sign up form
function validateSignUpForm(firstName, lastName, email, password, confirmPassword, agreeTerms) {
    let isValid = true;
    const errors = [];
    
    if (!firstName || firstName.trim() === '') {
        showFieldError('firstName', 'First name is required');
        errors.push('First name is required');
        isValid = false;
    }
    
    if (!lastName || lastName.trim() === '') {
        showFieldError('lastName', 'Last name is required');
        errors.push('Last name is required');
        isValid = false;
    }
    
    if (!email || !isValidEmail(email)) {
        showFieldError('signupEmail', 'Please enter a valid email address');
        errors.push('Please enter a valid email address');
        isValid = false;
    }
    
    if (!password || password.length < 6) {
        showFieldError('signupPassword', 'Password must be at least 6 characters');
        errors.push('Password must be at least 6 characters');
        isValid = false;
    }
    
    if (password !== confirmPassword) {
        showFieldError('confirmPassword', 'Passwords do not match');
        errors.push('Passwords do not match');
        isValid = false;
    }
    
    if (!agreeTerms) {
        errors.push('Please agree to the Terms of Service and Privacy Policy');
        isValid = false;
    }
    
    // Show all errors in alert if validation fails
    if (!isValid && errors.length > 0) {
        alert('Please fix the following errors:\n' + errors.join('\n'));
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

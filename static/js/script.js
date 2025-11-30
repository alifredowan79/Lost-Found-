// BUBT Lost and Found System - Main JavaScript
// Only essential functions that are actually used

// DOM Elements
const navLinks = document.querySelectorAll('.nav-link');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Check which page we're on and initialize accordingly
    const currentPage = window.location.pathname.split('/').pop() || '';
    
    if (currentPage === '' || currentPage === 'welcome.html' || currentPage === '/') {
        // Home/Welcome page
        initializeNavigation();
        makeHeroButtonsFunctional();
    } else if (currentPage === 'dashboard.html' || currentPage === 'dashboard') {
        // Dashboard page
        initializeDashboard();
    } else if (currentPage === 'report.html' || currentPage === 'report') {
        // Report page
        initializeReportTabs();
    } else if (currentPage === 'about.html' || currentPage === 'about') {
        // About page
        initializeNavigation();
    }
});

// Dashboard initialization
function initializeDashboard() {
    // Initialize main tabs
    initializeMainTabs();
    
    // Initialize module tabs
    const moduleTabs = document.querySelectorAll('.module-tab');
    moduleTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            const moduleContent = tab.closest('.module-content');
            
            if (!moduleContent) return;
            
            // Update active tab
            moduleContent.querySelectorAll('.module-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Update active content
            moduleContent.querySelectorAll('.module-tab-content').forEach(content => content.classList.remove('active'));
            const targetContent = moduleContent.querySelector(`#${targetTab}`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// Initialize main tabs
function initializeMainTabs() {
    const mainTabButtons = document.querySelectorAll('.main-tab-btn');
    const mainTabContents = document.querySelectorAll('.main-tab-content');
    
    mainTabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Update active tab button
            mainTabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update active tab content
            mainTabContents.forEach(content => content.classList.remove('active'));
            const targetContent = document.getElementById(`${targetTab}-tab`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });
}

// Toggle module visibility (used in dashboard)
function toggleModule(moduleId) {
    const moduleContent = document.getElementById(moduleId);
    const allModules = document.querySelectorAll('.module-content');
    
    if (!moduleContent) return;
    
    // Close all other modules
    allModules.forEach(module => {
        if (module.id !== moduleId) {
            module.classList.remove('active');
        }
    });
    
    // Toggle current module
    moduleContent.classList.toggle('active');
    
    // Update button text
    const button = event.target;
    if (moduleContent.classList.contains('active')) {
        button.innerHTML = '<i class="fas fa-eye-slash"></i> Hide';
    } else {
        button.innerHTML = '<i class="fas fa-eye"></i> View';
    }
}

// Make hero buttons functional (welcome page)
function makeHeroButtonsFunctional() {
    const goToDashboardBtn = document.querySelector('.hero .btn-primary');
    if (goToDashboardBtn) {
        goToDashboardBtn.addEventListener('click', () => {
            window.location.href = '/login';
        });
    }
    
    const reportLostBtn = document.querySelector('.hero .btn-secondary');
    if (reportLostBtn) {
        reportLostBtn.addEventListener('click', () => {
            window.location.href = '/login';
        });
    }
}

// Tab functionality for report page
function initializeReportTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Update active tab button
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update active tab content
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
}

// Navigation functionality
function initializeNavigation() {
    if (!navLinks.length || !navToggle || !navMenu) return;
    
    // Mobile navigation toggle
    navToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        navToggle.classList.toggle('active');
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        }
    });
}

// Add mobile navigation styles
const mobileNavStyles = `
    @media (max-width: 768px) {
        .nav-menu {
            position: fixed;
            top: 100%;
            left: 0;
            width: 100%;
            background: var(--bg-primary);
            box-shadow: var(--shadow-md);
            padding: 1rem 0;
            transform: translateY(-100%);
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }
        
        .nav-menu.active {
            transform: translateY(0);
            opacity: 1;
            visibility: visible;
        }
        
        .nav-toggle.active span:nth-child(1) {
            transform: rotate(45deg) translate(5px, 5px);
        }
        
        .nav-toggle.active span:nth-child(2) {
            opacity: 0;
        }
        
        .nav-toggle.active span:nth-child(3) {
            transform: rotate(-45deg) translate(7px, -6px);
        }
    }
`;

// Inject mobile navigation styles
const styleSheet = document.createElement('style');
styleSheet.textContent = mobileNavStyles;
document.head.appendChild(styleSheet);

console.log('BUBT Lost and Found System initialized successfully!');

// Sample data for demonstration
const sampleItems = [
    {
        id: 1,
        name: "iPhone 13 Pro",
        category: "electronics",
        status: "lost",
        date: "2024-01-15",
        location: "Main Library, 2nd Floor",
        description: "Black iPhone 13 Pro with blue case. Has a small scratch on the back.",
        contact: "john.doe@bubt.edu.bd",
        icon: "fas fa-mobile-alt"
    },
    {
        id: 2,
        name: "Gold Necklace",
        category: "jewelry",
        status: "found",
        date: "2024-01-14",
        location: "Student Center, Cafeteria",
        description: "Delicate gold chain necklace with a small pendant.",
        contact: "security@bubt.edu.bd",
        icon: "fas fa-gem"
    },
    {
        id: 3,
        name: "Car Keys",
        category: "keys",
        status: "lost",
        date: "2024-01-13",
        location: "Parking Lot A",
        description: "Toyota car keys with a black keychain.",
        contact: "jane.smith@bubt.edu.bd",
        icon: "fas fa-key"
    },
    {
        id: 4,
        name: "Laptop Charger",
        category: "electronics",
        status: "found",
        date: "2024-01-12",
        location: "Computer Lab, Room 205",
        description: "Dell laptop charger, black with white tip.",
        contact: "lab.assistant@bubt.edu.bd",
        icon: "fas fa-laptop"
    },
    {
        id: 5,
        name: "Student ID Card",
        category: "documents",
        status: "found",
        date: "2024-01-11",
        location: "Administration Building",
        description: "Student ID for Sarah Johnson, ID: 2024001",
        contact: "registrar@bubt.edu.bd",
        icon: "fas fa-id-card"
    },
    {
        id: 6,
        name: "Red Backpack",
        category: "clothing",
        status: "lost",
        date: "2024-01-10",
        location: "Gymnasium",
        description: "Red Jansport backpack with laptop compartment.",
        contact: "mike.wilson@bubt.edu.bd",
        icon: "fas fa-briefcase"
    }
];

// Generated invoices array
let generatedInvoices = [];
let invoiceCounter = 1001;

// DOM Elements
const tabButtons = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const searchInput = document.getElementById('search-input');
const searchBtn = document.querySelector('.search-btn');
const filterCategory = document.getElementById('filter-category');
const filterStatus = document.getElementById('filter-status');
const itemsGrid = document.getElementById('items-grid');
const navLinks = document.querySelectorAll('.nav-link');
const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');

// Dashboard elements
const totalItemsElement = document.getElementById('total-items');
const lostItemsElement = document.getElementById('lost-items');
const foundItemsElement = document.getElementById('found-items');
const totalInvoicesElement = document.getElementById('total-invoices');

// Main tab elements
const mainTabButtons = document.querySelectorAll('.main-tab-btn');
const mainTabContents = document.querySelectorAll('.main-tab-content');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Check which page we're on and initialize accordingly
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    
    if (currentPage === 'index.html') {
        // Home page
        initializeNavigation();
        makeHeroButtonsFunctional();
    } else if (currentPage === 'dashboard.html') {
        // Dashboard page
        initializeDashboard();
        updateDashboardStats();
        populateInvoiceItemSelect();
    } else if (currentPage === 'report.html') {
        // Report page
        initializeReportTabs();
        initializeForms();
    } else if (currentPage === 'search.html') {
        // Search page
        initializeSearch();
        populateItemsGrid(sampleItems);
    } else if (currentPage === 'invoice.html') {
        // Invoice page
        initializeInvoicePage();
    } else if (currentPage === 'about.html') {
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
    
    // Initialize dashboard forms
    initializeDashboardForms();
    
    // Set current date for invoice form
    document.getElementById('invoice-date').value = new Date().toISOString().split('T')[0];
    
    // Generate initial invoice number
    document.getElementById('invoice-number').value = `INV-${invoiceCounter}`;
}

// Open specific tab
function openTab(tabName) {
    // Find the main tab button for the specified tab
    const targetButton = document.querySelector(`[data-tab="${tabName}"]`);
    if (targetButton) {
        // Simulate click on the target tab button
        targetButton.click();
        
        // Scroll to the main tabs section
        const mainTabsSection = document.getElementById('main-tabs');
        if (mainTabsSection) {
            mainTabsSection.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// Make hero buttons functional
function makeHeroButtonsFunctional() {
    // "Go to Dashboard" button functionality
    const goToDashboardBtn = document.querySelector('.hero .btn-primary');
    if (goToDashboardBtn) {
        goToDashboardBtn.onclick = function() {
            window.location.href = 'dashboard.html';
        };
    }
    
    // "Report Lost Item" button functionality
    const reportLostBtn = document.querySelector('.hero .btn-secondary');
    if (reportLostBtn) {
        reportLostBtn.onclick = function() {
            window.location.href = 'report.html';
        };
    }
}

// Initialize main tabs
function initializeMainTabs() {
    const mainTabButtons = document.querySelectorAll('.main-tab-btn');
    const mainTabContents = document.querySelectorAll('.main-tab-content');
    
    if (!mainTabButtons.length || !mainTabContents.length) return;
    
    mainTabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');
            
            // Update active main tab button
            mainTabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            
            // Update active main tab content
            mainTabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${targetTab}-tab`).classList.add('active');
        });
    });
}

// Initialize dashboard forms
function initializeDashboardForms() {
    // Add item form
    const addItemForm = document.getElementById('add-item-form');
    if (addItemForm) {
        addItemForm.addEventListener('submit', handleAddItem);
    }
    
    // Invoice form
    const invoiceForm = document.getElementById('invoice-form');
    if (invoiceForm) {
        invoiceForm.addEventListener('submit', handleInvoiceGeneration);
    }
}

// Initialize invoice page
function initializeInvoicePage() {
    // Set current date for invoice form
    const invoiceDate = document.getElementById('invoice-date');
    if (invoiceDate) {
        invoiceDate.value = new Date().toISOString().split('T')[0];
    }
    
    // Generate initial invoice number
    const invoiceNumber = document.getElementById('invoice-number');
    if (invoiceNumber) {
        invoiceNumber.value = `INV-${invoiceCounter}`;
    }
    
    // Populate invoice item select
    populateInvoiceItemSelect();
    
    // Initialize invoice form
    const invoiceForm = document.getElementById('invoice-form');
    if (invoiceForm) {
        invoiceForm.addEventListener('submit', handleInvoiceGeneration);
    }
    
    // Populate invoices list
    populateInvoicesList();
}

// Handle add item form submission
function handleAddItem(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const newItem = {
        id: sampleItems.length + 1,
        name: formData.get('item-name'),
        category: formData.get('item-category'),
        status: formData.get('item-status'),
        date: formData.get('item-date'),
        location: formData.get('item-location'),
        description: formData.get('item-description'),
        contact: formData.get('item-contact'),
        icon: getCategoryIcon(formData.get('item-category'))
    };
    
    // Add to sample items
    sampleItems.unshift(newItem);
    
    // Update all displays
    populateItemsGrid(sampleItems);
    updateDashboardStats();
    populateItemsTable();
    populateLostItemsGrid();
    populateFoundItemsGrid();
    populateInvoiceItemSelect();
    
    // Show success message
    showMessage('Item added successfully!', 'success');
    
    // Reset form
    e.target.reset();
}

// Handle invoice generation
function handleInvoiceGeneration(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const selectedItemId = formData.get('invoice-item');
    const selectedItem = sampleItems.find(item => item.id == selectedItemId);
    
    if (!selectedItem) {
        showMessage('Please select a valid item', 'error');
        return;
    }
    
    const newInvoice = {
        id: invoiceCounter++,
        invoiceNumber: `INV-${invoiceCounter - 1}`,
        itemId: selectedItem.id,
        itemName: selectedItem.name,
        itemCategory: selectedItem.category,
        date: formData.get('invoice-date'),
        amount: parseFloat(formData.get('invoice-amount')),
        notes: formData.get('invoice-notes'),
        status: 'pending'
    };
    
    // Add to invoices array
    generatedInvoices.unshift(newInvoice);
    
    // Update displays
    updateDashboardStats();
    populateInvoicesList();
    
    // Show success message
    showMessage('Invoice generated successfully!', 'success');
    
    // Reset form and update invoice number
    e.target.reset();
    document.getElementById('invoice-date').value = new Date().toISOString().split('T')[0];
    document.getElementById('invoice-number').value = `INV-${invoiceCounter}`;
    document.getElementById('invoice-amount').value = '5.00';
}

// Update dashboard statistics
function updateDashboardStats() {
    const totalItems = sampleItems.length;
    const lostItems = sampleItems.filter(item => item.status === 'lost').length;
    const foundItems = sampleItems.filter(item => item.status === 'found').length;
    const totalInvoices = generatedInvoices.length;
    
    totalItemsElement.textContent = totalItems;
    lostItemsElement.textContent = lostItems;
    foundItemsElement.textContent = foundItems;
    totalInvoicesElement.textContent = totalInvoices;
}

// Populate items table
function populateItemsTable() {
    const tableBody = document.getElementById('items-table-body');
    if (!tableBody) return;
    
    tableBody.innerHTML = sampleItems.map(item => `
        <tr>
            <td>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <i class="${item.icon}" style="color: var(--primary-color);"></i>
                    <strong>${item.name}</strong>
                </div>
            </td>
            <td><span class="item-category">${item.category}</span></td>
            <td>
                <span style="color: ${item.status === 'lost' ? 'var(--warning-color)' : 'var(--success-color)'}; font-weight: 600;">
                    ${item.status.toUpperCase()}
                </span>
            </td>
            <td>${formatDate(item.date)}</td>
            <td>${item.location}</td>
            <td>
                <button class="btn btn-primary" onclick="viewItemDetails(${item.id})" style="padding: 0.5rem 1rem; font-size: 0.875rem;">
                    <i class="fas fa-eye"></i> View
                </button>
            </td>
        </tr>
    `).join('');
}

// Populate lost items grid
function populateLostItemsGrid() {
    const lostGrid = document.getElementById('lost-items-grid');
    if (!lostGrid) return;
    
    const lostItems = sampleItems.filter(item => item.status === 'lost');
    
    if (lostItems.length === 0) {
        lostGrid.innerHTML = '<p style="color: var(--text-light); text-align: center; grid-column: 1 / -1;">No lost items found</p>';
        return;
    }
    
    lostGrid.innerHTML = lostItems.map(item => `
        <div class="lost-item-card">
            <div class="item-card-header">
                <div class="item-card-title">${item.name}</div>
                <span class="item-card-status lost">LOST</span>
            </div>
            <div class="item-card-details">
                <p><strong>Category:</strong> ${item.category}</p>
                <p><strong>Date Lost:</strong> ${formatDate(item.date)}</p>
                <p><strong>Location:</strong> ${item.location}</p>
                <p><strong>Contact:</strong> ${item.contact}</p>
            </div>
        </div>
    `).join('');
}

// Populate found items grid
function populateFoundItemsGrid() {
    const foundGrid = document.getElementById('found-items-grid');
    if (!foundGrid) return;
    
    const foundItems = sampleItems.filter(item => item.status === 'found');
    
    if (foundItems.length === 0) {
        foundGrid.innerHTML = '<p style="color: var(--text-light); text-align: center; grid-column: 1 / -1;">No found items found</p>';
        return;
    }
    
    foundGrid.innerHTML = foundItems.map(item => `
        <div class="found-item-card">
            <div class="item-card-header">
                <div class="item-card-title">${item.name}</div>
                <span class="item-card-status found">FOUND</span>
            </div>
            <div class="item-card-details">
                <p><strong>Category:</strong> ${item.category}</p>
                <p><strong>Date Found:</strong> ${formatDate(item.date)}</p>
                <p><strong>Location:</strong> ${item.location}</p>
                <p><strong>Contact:</strong> ${item.contact}</p>
            </div>
        </div>
    `).join('');
}

// Populate invoice item select
function populateInvoiceItemSelect() {
    const invoiceItemSelect = document.getElementById('invoice-item');
    if (!invoiceItemSelect) return;
    
    const foundItems = sampleItems.filter(item => item.status === 'found');
    
    // Clear existing options except the first one
    invoiceItemSelect.innerHTML = '<option value="">Choose a found item</option>';
    
    foundItems.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = `${item.name} - ${item.category} (${item.location})`;
        invoiceItemSelect.appendChild(option);
    });
}

// Populate invoices list
function populateInvoicesList() {
    const invoicesList = document.getElementById('invoices-list');
    if (!invoicesList) return;
    
    if (generatedInvoices.length === 0) {
        invoicesList.innerHTML = '<p style="color: var(--text-light); text-align: center;">No invoices generated yet</p>';
        return;
    }
    
    invoicesList.innerHTML = generatedInvoices.map(invoice => `
        <div class="invoice-item">
            <div class="invoice-header">
                <span class="invoice-number">${invoice.invoiceNumber}</span>
                <span class="invoice-date">${formatDate(invoice.date)}</span>
            </div>
            <div class="invoice-details">
                <p><strong>Item:</strong> ${invoice.itemName}</p>
                <p><strong>Category:</strong> ${invoice.itemCategory}</p>
                <p><strong>Notes:</strong> ${invoice.notes || 'No additional notes'}</p>
            </div>
            <div class="invoice-amount">
                Processing Fee: $${invoice.amount.toFixed(2)}
            </div>
        </div>
    `).join('');
}

// Toggle module visibility
function toggleModule(moduleId) {
    const moduleContent = document.getElementById(moduleId);
    const allModules = document.querySelectorAll('.module-content');
    
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
        
        // Populate data when opening module
        if (moduleId === 'item-management') {
            populateItemsTable();
        } else if (moduleId === 'lost-products') {
            populateLostItemsGrid();
        } else if (moduleId === 'found-products') {
            populateFoundItemsGrid();
        } else if (moduleId === 'invoice-generation') {
            populateInvoicesList();
        }
    } else {
        button.innerHTML = '<i class="fas fa-eye"></i> View';
    }
}

// View item details
function viewItemDetails(itemId) {
    const item = sampleItems.find(item => item.id === itemId);
    if (!item) return;
    
    const details = `
Item: ${item.name}
Category: ${item.category}
Status: ${item.status.toUpperCase()}
Date: ${formatDate(item.date)}
Location: ${item.location}
Description: ${item.description}
Contact: ${item.contact}
    `;
    
    alert(details);
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

// Tab functionality for dashboard page
function initializeTabs() {
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

// Search and filter functionality
function initializeSearch() {
    const searchBtn = document.querySelector('.search-btn');
    const searchInput = document.getElementById('search-input');
    const filterCategory = document.getElementById('filter-category');
    const filterStatus = document.getElementById('filter-status');
    
    if (!searchBtn || !searchInput || !filterCategory || !filterStatus) return;
    
    // Search button click
    searchBtn.addEventListener('click', performSearch);
    
    // Enter key in search input
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Filter changes
    filterCategory.addEventListener('change', performSearch);
    filterStatus.addEventListener('change', performSearch);
}

function performSearch() {
    const searchInput = document.getElementById('search-input');
    const filterCategory = document.getElementById('filter-category');
    const filterStatus = document.getElementById('filter-status');
    
    if (!searchInput || !filterCategory || !filterStatus) return;
    
    const searchTerm = searchInput.value.toLowerCase();
    const categoryFilter = filterCategory.value;
    const statusFilter = filterStatus.value;
    
    let filteredItems = sampleItems.filter(item => {
        const matchesSearch = item.name.toLowerCase().includes(searchTerm) ||
                            item.description.toLowerCase().includes(searchTerm) ||
                            item.location.toLowerCase().includes(searchTerm);
        
        const matchesCategory = !categoryFilter || item.category === categoryFilter;
        const matchesStatus = !statusFilter || item.status === statusFilter;
        
        return matchesSearch && matchesCategory && matchesStatus;
    });
    
    populateItemsGrid(filteredItems);
}

function clearFilters() {
    const searchInput = document.getElementById('search-input');
    const filterCategory = document.getElementById('filter-category');
    const filterStatus = document.getElementById('filter-status');
    
    if (!searchInput || !filterCategory || !filterStatus) return;
    
    searchInput.value = '';
    filterCategory.value = '';
    filterStatus.value = '';
    populateItemsGrid(sampleItems);
}

// Populate items grid
function populateItemsGrid(items) {
    if (items.length === 0) {
        itemsGrid.innerHTML = `
            <div class="text-center" style="grid-column: 1 / -1; padding: 3rem;">
                <i class="fas fa-search" style="font-size: 3rem; color: var(--text-light); margin-bottom: 1rem;"></i>
                <h3 style="color: var(--text-secondary); margin-bottom: 0.5rem;">No items found</h3>
                <p style="color: var(--text-light);">Try adjusting your search criteria or filters.</p>
            </div>
        `;
        return;
    }
    
    itemsGrid.innerHTML = items.map(item => `
        <div class="item-card">
            <div class="item-image">
                <i class="${item.icon}"></i>
            </div>
            <div class="item-content">
                <h3 class="item-title">${item.name}</h3>
                <span class="item-category">${item.category}</span>
                <div class="item-details">
                    <p><strong>Status:</strong> <span style="color: ${item.status === 'lost' ? 'var(--danger-color)' : 'var(--success-color)'}">${item.status.toUpperCase()}</span></p>
                    <p><strong>Date:</strong> ${formatDate(item.date)}</p>
                    <p><strong>Location:</strong> ${item.location}</p>
                </div>
                <p class="item-description">${item.description}</p>
                <button class="btn btn-primary" onclick="contactOwner('${item.contact}', '${item.name}')">
                    <i class="fas fa-envelope"></i> Contact Owner
                </button>
            </div>
        </div>
    `).join('');
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Navigation functionality
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
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

// Enhanced scroll to section function
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        // Update active navigation link
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${sectionId}`) {
                link.classList.add('active');
            }
        });
        
        // Smooth scroll to section
        section.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
        
        // Add a small highlight effect
        section.style.transition = 'all 0.3s ease';
        section.style.transform = 'scale(1.02)';
        setTimeout(() => {
            section.style.transform = 'scale(1)';
        }, 300);
    }
}

// Form functionality
function initializeForms() {
    const forms = document.querySelectorAll('.report-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
}

function handleFormSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const formObject = {};
    
    formData.forEach((value, key) => {
        formObject[key] = value;
    });
    
    // Simulate form submission
    showMessage('Thank you! Your report has been submitted successfully.', 'success');
    
    // Reset form
    e.target.reset();
    
    // Add new item to sample data (for demo purposes)
    const newItem = {
        id: sampleItems.length + 1,
        name: formObject['item-name'] || formObject['found-item-name'],
        category: formObject['category'] || formObject['found-category'],
        status: e.target.id === 'lost-tab' ? 'lost' : 'found',
        date: formObject['date-lost'] || formObject['date-found'],
        location: formObject['location'] || formObject['found-location'],
        description: formObject['description'] || formObject['found-description'],
        contact: formObject['contact'] || formObject['found-contact'],
        icon: getCategoryIcon(formObject['category'] || formObject['found-category'])
    };
    
    sampleItems.unshift(newItem);
    populateItemsGrid(sampleItems);
    updateDashboardStats();
    populateItemsTable();
    populateLostItemsGrid();
    populateFoundItemsGrid();
    populateInvoiceItemSelect();
}

// Get icon for category
function getCategoryIcon(category) {
    const iconMap = {
        'electronics': 'fas fa-laptop',
        'jewelry': 'fas fa-gem',
        'clothing': 'fas fa-tshirt',
        'documents': 'fas fa-file-alt',
        'keys': 'fas fa-key',
        'other': 'fas fa-question-circle'
    };
    
    return iconMap[category] || 'fas fa-question-circle';
}

// Show message
function showMessage(message, type = 'success') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    // Insert message at the top of the form
    const activeForm = document.querySelector('.tab-content.active .report-form, .module-tab-content.active form');
    if (activeForm) {
        activeForm.insertBefore(messageDiv, activeForm.firstChild);
        
        // Remove message after 5 seconds
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

// Contact owner function
function contactOwner(contact, itemName) {
    const message = `Contact information for ${itemName}: ${contact}`;
    alert(message); // In a real application, this would open a contact form or modal
}

// Add some CSS for mobile navigation
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

// Add scroll spy for navigation highlighting
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const scrollPos = window.scrollY + 100;
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');
        
        if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
});

// Add loading states and animations
function addLoadingState(element) {
    element.classList.add('loading');
    element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
}

function removeLoadingState(element, originalContent) {
    element.classList.remove('loading');
    element.innerHTML = originalContent;
}

// Add some interactive features
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effects to floating cards
    const floatingCards = document.querySelectorAll('.floating-card');
    floatingCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'scale(1.05)';
            card.style.boxShadow = '0 20px 40px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'scale(1)';
            card.style.boxShadow = 'var(--shadow-lg)';
        });
        
        // Add click functionality to floating cards
        card.addEventListener('click', () => {
            const cardText = card.querySelector('span').textContent;
            if (cardText === 'Lost Phone') {
                window.location.href = 'report.html';
            } else if (cardText === 'Lost Keys') {
                window.location.href = 'search.html';
            } else if (cardText === 'Lost Wallet') {
                window.location.href = 'dashboard.html';
            }
        });
        
        // Add cursor pointer to show cards are clickable
        card.style.cursor = 'pointer';
    });
    
    // Add form validation feedback
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            if (input.hasAttribute('required') && !input.value.trim()) {
                input.style.borderColor = 'var(--danger-color)';
                showInputError(input, 'This field is required');
            } else {
                input.style.borderColor = 'var(--border-color)';
                removeInputError(input);
            }
        });
        
        input.addEventListener('input', () => {
            if (input.style.borderColor === 'var(--danger-color)') {
                input.style.borderColor = 'var(--border-color)';
                removeInputError(input);
            }
        });
        
        // Add focus effects
        input.addEventListener('focus', () => {
            input.style.boxShadow = '0 0 0 3px rgba(37, 99, 235, 0.1)';
        });
        
        input.addEventListener('blur', () => {
            input.style.boxShadow = 'none';
        });
    });
    
    // Add button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0)';
        });
    });
    
    // Add statistics counter animation
    animateStatistics();
});

// Show input error message
function showInputError(input, message) {
    // Remove existing error
    removeInputError(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'input-error';
    errorDiv.textContent = message;
    errorDiv.style.color = 'var(--danger-color)';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';
    
    input.parentNode.appendChild(errorDiv);
}

// Remove input error message
function removeInputError(input) {
    const existingError = input.parentNode.querySelector('.input-error');
    if (existingError) {
        existingError.remove();
    }
}

// Animate statistics counters
function animateStatistics() {
    const statNumbers = document.querySelectorAll('.stat-content h3');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = parseInt(target.textContent);
                animateCounter(target, 0, finalValue, 1000);
                observer.unobserve(target);
            }
        });
    });
    
    statNumbers.forEach(stat => observer.observe(stat));
}

// Counter animation function
function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

console.log('BUBT Lost and Found System with Dashboard initialized successfully!');

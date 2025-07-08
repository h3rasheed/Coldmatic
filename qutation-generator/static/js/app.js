// /**
//  * Coldmatic Door Quotation System - Main JavaScript
//  */

// class QuotationApp {
//     constructor() {
//         this.form = document.getElementById('quoteForm');
//         this.step2Section = document.getElementById('step2Section');
//         this.completeStep1Btn = document.getElementById('completeStep1');
//         this.expandStep2Btn = document.getElementById('expandStep2Btn');
//         this.generateQuoteBtn = document.getElementById('generateQuoteBtn');
        
//         this.requiredStep1Fields = [
//             'door_type', 'cooler_freezer', 'frame_structure', 'motorized_manual',
//             'width_inches', 'height_inches', 'depth_inches', 'wall_thickness_inches',
//             'customer_name', 'customer_address'
//         ];
        
//         this.isStep1Complete = false;
//         this.currentPricing = {};
        
//         this.init();
//     }
    
//     init() {
//         this.setupEventListeners();
//         this.setupFormValidation();
//         this.calculatePrice();
//     }
    
//     setupEventListeners() {
//         // Step 1 completion
//         if (this.completeStep1Btn) {
//             this.completeStep1Btn.addEventListener('click', () => this.completeStep1());
//         }
        
//         // Real-time price calculation
//         if (this.form) {
//             const priceInputs = this.form.querySelectorAll('input, select');
//             priceInputs.forEach(input => {
//                 input.addEventListener('change', () => this.calculatePrice());
//                 input.addEventListener('input', () => this.debounceCalculatePrice());
//             });
//         }
        
//         // Sliding door package toggle
//         const slidingDoorPackage = document.querySelector('input[name="sliding_door_package"]');
//         if (slidingDoorPackage) {
//             slidingDoorPackage.addEventListener('change', () => this.toggleSlidingDoorOptions());
//         }
        
//         // Door type specific options
//         const doorTypeSelect = document.getElementById('doorType');
//         const coolerFreezerSelect = document.getElementById('coolerFreezer');
//         if (doorTypeSelect) {
//             doorTypeSelect.addEventListener('change', () => this.handleDoorTypeChange());
//         }
//         if (coolerFreezerSelect) {
//             coolerFreezerSelect.addEventListener('change', () => this.handleCoolerFreezerChange());
//         }
        
//         // Form submission
//         if (this.form) {
//             this.form.addEventListener('submit', (e) => this.handleFormSubmit(e));
//         }
        
//         // Step 2 collapse events
//         if (this.step2Section) {
//             this.step2Section.addEventListener('shown.bs.collapse', () => {
//                 this.expandStep2Btn.style.display = 'none';
//             });
            
//             this.step2Section.addEventListener('hidden.bs.collapse', () => {
//                 if (!this.isStep1Complete) {
//                     this.expandStep2Btn.style.display = 'block';
//                 }
//             });
//         }
//     }
    
//     setupFormValidation() {
//         // Add real-time validation for required fields
//         this.requiredStep1Fields.forEach(fieldName => {
//             const field = document.querySelector(`[name="${fieldName}"]`);
//             if (field) {
//                 field.addEventListener('blur', () => this.validateField(field));
//                 field.addEventListener('input', () => this.clearFieldError(field));
//             }
//         });
//     }
    
//     validateField(field) {
//         if (!field.value || field.value.trim() === '') {
//             this.showFieldError(field, 'This field is required');
//             return false;
//         } else {
//             this.clearFieldError(field);
//             return true;
//         }
//     }
    
//     showFieldError(field, message) {
//         field.classList.add('is-invalid');
        
//         // Remove existing error message
//         const existingError = field.parentNode.querySelector('.invalid-feedback');
//         if (existingError) {
//             existingError.remove();
//         }
        
//         // Add new error message
//         const errorDiv = document.createElement('div');
//         errorDiv.className = 'invalid-feedback';
//         errorDiv.textContent = message;
//         field.parentNode.appendChild(errorDiv);
//     }
    
//     clearFieldError(field) {
//         field.classList.remove('is-invalid');
//         const errorDiv = field.parentNode.querySelector('.invalid-feedback');
//         if (errorDiv) {
//             errorDiv.remove();
//         }
//     }
    
//     completeStep1() {
//         // Validate all required Step 1 fields
//         let isValid = true;
        
//         this.requiredStep1Fields.forEach(fieldName => {
//             const field = document.querySelector(`[name="${fieldName}"]`);
//             if (field && !this.validateField(field)) {
//                 isValid = false;
//             }
//         });
        
//         if (isValid) {
//             this.isStep1Complete = true;
            
//             // Update Step 1 button
//             this.completeStep1Btn.innerHTML = '<i class="fas fa-check me-2"></i>Step 1 Complete ✓';
//             this.completeStep1Btn.classList.remove('btn-success');
//             this.completeStep1Btn.classList.add('btn-outline-success');
//             this.completeStep1Btn.disabled = true;
            
//             // Expand Step 2
//             const step2Collapse = new bootstrap.Collapse(this.step2Section, {show: true});
            
//             // Hide expand button
//             if (this.expandStep2Btn) {
//                 this.expandStep2Btn.style.display = 'none';
//             }
            
//             // Smooth scroll to Step 2
//             setTimeout(() => {
//                 this.step2Section.scrollIntoView({ 
//                     behavior: 'smooth', 
//                     block: 'start' 
//                 });
//             }, 350);
            
//         } else {
//             this.showAlert('Please complete all required fields in Step 1', 'warning');
//         }
//     }
    
//     toggleSlidingDoorOptions() {
//         const slidingDoorPackage = document.querySelector('input[name="sliding_door_package"]');
//         const slidingDoorOptions = document.getElementById('slidingDoorOptions');
        
//         if (slidingDoorOptions) {
//             slidingDoorOptions.style.display = slidingDoorPackage.checked ? 'block' : 'none';
//         }
//     }
    
//     handleDoorTypeChange() {
//         const doorType = document.getElementById('doorType').value;
//         const motorizedManual = document.querySelector('[name="motorized_manual"]');
        
//         // Update available options based on door type
//         if (doorType === 'Power Operated Sliding door - Single horizontal') {
//             if (motorizedManual) {
//                 motorizedManual.value = 'Motorized';
//                 motorizedManual.disabled = true;
//             }
//         } else {
//             if (motorizedManual) {
//                 motorizedManual.disabled = false;
//             }
//         }
        
//         this.calculatePrice();
//     }
    
//     handleCoolerFreezerChange() {
//         const coolerFreezer = document.getElementById('coolerFreezer').value;
//         const freezerMotorVolts = document.querySelector('[name="freezer_door_motor_volts"]');
        
//         // Show/hide freezer-specific options
//         if (freezerMotorVolts) {
//             const container = freezerMotorVolts.closest('.col-md-6');
//             if (container) {
//                 container.style.display = coolerFreezer === 'Freezer' ? 'block' : 'none';
//             }
//         }
        
//         this.calculatePrice();
//     }
    
//     debounceCalculatePrice() {
//         clearTimeout(this.priceCalculationTimeout);
//         this.priceCalculationTimeout = setTimeout(() => {
//             this.calculatePrice();
//         }, 500);
//     }
    
//     async calculatePrice() {
//         // if (!this.form) return;
        
//         // try {
//         //     const formData = new FormData(this.form);
//         //     const data = this.processFormData(formData);
            
//         //     const response = await fetch('/calculate_price', {
//         //         method: 'POST',
//         //         headers: {
//         //             'Content-Type': 'application/json',
//         //         },
//         //         body: JSON.stringify(data)
//         //     });
            
//         //     const result = await response.json();
            
//         //     if (result.success) {
//         //         this.currentPricing = result.pricing;
//         //         this.updatePricingDisplay(result.pricing);
//         //     } else {
//         //         console.error('Price calculation failed:', result.error);
//         //     }
//         // } catch (error) {
//         //     console.error('Price calculation error:', error);
//         // }
//     }
    
//     processFormData(formData) {
//         const data = {};
        
//         for (let [key, value] of formData.entries()) {
//             const input = document.querySelector(`[name="${key}"]`);
            
//             if (key.endsWith('_inches') || key === 'quantity') {
//                 data[key] = parseInt(value) || 0;
//             } else if (input && input.type === 'checkbox') {
//                 data[key] = value === 'y';
//             } else {
//                 data[key] = value;
//             }
//         }
        
//         return data;
//     }
    
//     updatePricingDisplay(pricing) {
//         const elements = {
//             'basePrice': pricing.base_price,
//             'materialCost': pricing.material_cost,
//             'hardwareCost': pricing.hardware_cost,
//             'laborCost': pricing.labor_cost,
//             'totalPrice': pricing.total_price
//         };
        
//         Object.entries(elements).forEach(([elementId, value]) => {
//             const element = document.getElementById(elementId);
//             if (element) {
//                 element.textContent = `$${value.toFixed(2)}`;
                
//                 // Add animation effect
//                 element.style.transform = 'scale(1.05)';
//                 element.style.transition = 'transform 0.2s ease';
//                 setTimeout(() => {
//                     element.style.transform = 'scale(1)';
//                 }, 200);
//             }
//         });
//     }
    
//     handleFormSubmit(e) {
//         // Add loading state to submit button
//         if (this.generateQuoteBtn) {
//             this.generateQuoteBtn.disabled = true;
//             this.generateQuoteBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating Quote...';
//         }
        
//         // Form will be submitted normally
//     }
    
//     showAlert(message, type = 'info') {
//         // Create alert element
//         const alertDiv = document.createElement('div');
//         alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
//         alertDiv.innerHTML = `
//             ${message}
//             <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
//         `;
        
//         // Insert at top of main container
//         const mainContainer = document.querySelector('main .container');
//         if (mainContainer) {
//             mainContainer.insertBefore(alertDiv, mainContainer.firstChild);
            
//             // Auto-dismiss after 5 seconds
//             setTimeout(() => {
//                 if (alertDiv.parentNode) {
//                     alertDiv.remove();
//                 }
//             }, 5000);
//         }
//     }
// }

// // Utility functions
// function formatCurrency(amount) {
//     return new Intl.NumberFormat('en-CA', {
//         style: 'currency',
//         currency: 'CAD'
//     }).format(amount);
// }

// function validateEmail(email) {
//     const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//     return re.test(email);
// }

// function validatePhone(phone) {
//     const re = /^[\+]?[\d\s\-\(\)]+$/;
//     return re.test(phone);
// }

// // Initialize the application when DOM is loaded
// document.addEventListener('DOMContentLoaded', function() {
//     new QuotationApp();
    
//     // Initialize Bootstrap tooltips
//     const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
//     tooltipTriggerList.map(function (tooltipTriggerEl) {
//         return new bootstrap.Tooltip(tooltipTriggerEl);
//     });
    
//     // Initialize Bootstrap popovers
//     const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
//     popoverTriggerList.map(function (popoverTriggerEl) {
//         return new bootstrap.Popover(popoverTriggerEl);
//     });
// });

// // Export for testing purposes
// if (typeof module !== 'undefined' && module.exports) {
//     module.exports = { QuotationApp, formatCurrency, validateEmail, validatePhone };
// }

// Enhanced JavaScript for Tearsheet with Bootstrap validation
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    
    if (form) {
        // Bootstrap form validation
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            event.stopPropagation();

            // Custom validation logic
            let isValid = validateForm();
            
            if (isValid && form.checkValidity()) {
                showLoadingState();
                // Allow form submission
                form.submit();
            }
            
            form.classList.add('was-validated');
        }, false);

        // Real-time weight validation
        const weightInputs = form.querySelectorAll('input[name="weights[]"]');
        weightInputs.forEach(input => {
            input.addEventListener('input', validateWeights);
            input.addEventListener('blur', validateWeights);
        });

        // Symbol input validation
        const symbolInputs = form.querySelectorAll('input[name="symbols[]"]');
        symbolInputs.forEach(input => {
            input.addEventListener('input', validateSymbol);
        });

        // Date validation
        const startDateInput = document.getElementById('start_date');
        const endDateInput = document.getElementById('end_date');
        
        if (startDateInput && endDateInput) {
            startDateInput.addEventListener('change', validateDateRange);
            endDateInput.addEventListener('change', validateDateRange);
        }

        // Capital input formatting
        const capitalInput = document.getElementById('capital');
        if (capitalInput) {
            capitalInput.addEventListener('input', formatCapital);
        }
    }

    // Form validation functions
    function validateForm() {
        let isValid = true;

        // Validate portfolio weights
        if (!validateWeights()) {
            isValid = false;
        }

        // Validate date range
        if (!validateDateRange()) {
            isValid = false;
        }

        // Validate symbols
        const symbolInputs = document.querySelectorAll('input[name="symbols[]"]');
        symbolInputs.forEach(input => {
            if (!validateSymbol(input)) {
                isValid = false;
            }
        });

        return isValid;
    }

    function validateWeights() {
        const weightInputs = document.querySelectorAll('input[name="weights[]"]');
        const weightAlert = document.querySelector('.alert-info');
        let totalWeight = 0;
        let hasValidWeights = true;

        weightInputs.forEach(input => {
            const value = parseFloat(input.value);
            const feedbackDiv = input.parentNode.parentNode.querySelector('.invalid-feedback');
            
            if (isNaN(value) || value < 0 || value > 1) {
                input.setCustomValidity('Weight must be between 0 and 1');
                hasValidWeights = false;
            } else {
                input.setCustomValidity('');
                totalWeight += value;
            }
        });

        // Check if weights sum to 1.0
        const weightSumValid = Math.abs(totalWeight - 1.0) < 0.0001;
        
        if (!weightSumValid && hasValidWeights) {
            weightInputs.forEach(input => {
                input.setCustomValidity('Portfolio weights must sum to 1.0');
            });
            hasValidWeights = false;
        } else if (weightSumValid) {
            weightInputs.forEach(input => {
                if (input.checkValidity()) {
                    input.setCustomValidity('');
                }
            });
        }

        // Update alert styling
        if (weightAlert) {
            if (weightSumValid) {
                weightAlert.className = 'alert alert-success d-flex align-items-center';
                weightAlert.innerHTML = '<i class="bi bi-check-circle-fill me-2"></i><div>Portfolio weights are perfectly balanced (100%)</div>';
            } else {
                weightAlert.className = 'alert alert-warning d-flex align-items-center';
                weightAlert.innerHTML = `<i class="bi bi-exclamation-triangle-fill me-2"></i><div>Current total: ${(totalWeight * 100).toFixed(1)}% (must equal 100%)</div>`;
            }
        }

        return hasValidWeights && weightSumValid;
    }

    function validateDateRange() {
        const startDate = document.getElementById('start_date');
        const endDate = document.getElementById('end_date');
        
        if (!startDate || !endDate) return true;

        const start = new Date(startDate.value);
        const end = new Date(endDate.value);
        const today = new Date();
        
        let isValid = true;

        // Check if start date is not in the future
        if (start > today) {
            startDate.setCustomValidity('Start date cannot be in the future');
            isValid = false;
        } else {
            startDate.setCustomValidity('');
        }

        // Check if end date is not in the future
        if (end > today) {
            endDate.setCustomValidity('End date cannot be in the future');
            isValid = false;
        } else {
            endDate.setCustomValidity('');
        }

        // Check if start date is before end date
        if (start >= end) {
            endDate.setCustomValidity('End date must be after start date');
            isValid = false;
        } else if (endDate.checkValidity()) {
            endDate.setCustomValidity('');
        }

        // Check for minimum period (at least 30 days)
        const daysDiff = (end - start) / (1000 * 60 * 60 * 24);
        if (daysDiff < 30) {
            endDate.setCustomValidity('Analysis period must be at least 30 days');
            isValid = false;
        }

        return isValid;
    }

    function validateSymbol(inputElement) {
        const input = inputElement.target || inputElement;
        const value = input.value.trim().toUpperCase();
        
        // Vietnam stock symbol validation (3-4 characters, letters only)
        const symbolPattern = /^[A-Z]{3,4}$/;
        
        if (!value) {
            input.setCustomValidity('Stock symbol is required');
            return false;
        } else if (!symbolPattern.test(value)) {
            input.setCustomValidity('Enter a valid Vietnam stock symbol (3-4 letters)');
            return false;
        } else {
            input.setCustomValidity('');
            input.value = value; // Convert to uppercase
            return true;
        }
    }

    function formatCapital() {
        const input = document.getElementById('capital');
        if (!input) return;

        const value = parseInt(input.value);
        
        // Update the display 
        const display = input.parentNode.querySelector('.form-text');
        if (display && value) {
            if (value >= 1000000) {
                const millions = (value / 1000000).toFixed(1);
                display.textContent = `Investment: ₫${millions}M VND`;
                display.className = 'form-text text-success';
            } else {
                display.textContent = 'Minimum investment: ₫1,000,000 (1 million VND)';
                display.className = 'form-text text-muted';
            }
        }
    }

    function showLoadingState() {
        const submitBtn = document.querySelector('button[type="submit"]');
        const spinner = submitBtn.querySelector('.spinner-border');
        
        if (submitBtn && spinner) {
            submitBtn.disabled = true;
            spinner.classList.remove('d-none');
            submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Analyzing... <span class="spinner-border spinner-border-sm ms-2" role="status"></span>';
        }
    }

    // Auto-save form data to localStorage (optional enhancement)
    function saveFormData() {
        const formData = new FormData(document.querySelector('form'));
        const data = {};
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }
        localStorage.setItem('tearsheet_form_data', JSON.stringify(data));
    }

    function loadFormData() {
        const savedData = localStorage.getItem('tearsheet_form_data');
        if (savedData && confirm('Would you like to restore your previous portfolio configuration?')) {
            const data = JSON.parse(savedData);
            Object.keys(data).forEach(key => {
                const inputs = document.querySelectorAll(`[name="${key}"]`);
                if (inputs.length > 1) {
                    // Handle arrays (symbols[], weights[])
                    inputs.forEach((input, index) => {
                        if (data[key][index]) {
                            input.value = data[key][index];
                        }
                    });
                } else if (inputs.length === 1) {
                    inputs[0].value = data[key];
                }
            });
        }
    }

    // Initialize form data loading
    if (window.location.pathname === '/') {
        loadFormData();
    }

    // Save form data on input (debounced)
    let saveTimeout;
    function debouncedSave() {
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(saveFormData, 1000);
    }

    const inputs = document.querySelectorAll('form input');
    inputs.forEach(input => {
        input.addEventListener('input', debouncedSave);
    });
});
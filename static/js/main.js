// Global variables
let currentPage = 1;
let totalPages = 1;
let currentFilters = {};
let isLoading = false;

// Initialize the application
function initializeFilters() {
    loadCities();
    loadBuildingTypes();
    loadLayouts();
    setupEventListeners();
}

// Setup event listeners
function setupEventListeners() {
    // Search mode toggle
    document.querySelectorAll('input[name="search-mode"]').forEach(radio => {
        radio.addEventListener('change', toggleSearchMode);
    });
    
    // Traditional search button
    document.getElementById('search-btn').addEventListener('click', performSearch);
    
    // Smart search button
    document.getElementById('smart-search-btn').addEventListener('click', performSmartSearch);
    
    // Keyword search on Enter
    document.getElementById('keyword-search').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // Smart query on Enter
    document.getElementById('smart-query').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            performSmartSearch();
        }
    });
    
    // City change event
    document.getElementById('city-filter').addEventListener('change', function() {
        const selectedCity = this.value;
        if (selectedCity) {
            loadDistricts(selectedCity);
        } else {
            document.getElementById('district-filter').innerHTML = '<option value="">選擇地區</option>';
        }
    });
    
    // Apply filters button
    document.getElementById('apply-filters').addEventListener('click', applyFilters);
    
    // Clear filters button
    document.getElementById('clear-filters').addEventListener('click', clearFilters);
    
    // Sort change event
    document.getElementById('sort-by').addEventListener('change', function() {
        currentFilters.sort_by = this.value;
        currentPage = 1;
        loadListings();
    });
    
    // Page size change event
    document.getElementById('page-size').addEventListener('change', function() {
        currentPage = 1;
        loadListings();
    });
    
    // Smart search sliders
    document.getElementById('alpha-slider').addEventListener('input', function() {
        document.getElementById('alpha-value').textContent = this.value + '% 文字';
    });
    
    document.getElementById('threshold-slider').addEventListener('input', function() {
        document.getElementById('threshold-value').textContent = this.value + '% 相似度';
    });
    
    // Image upload preview
    document.getElementById('reference-image').addEventListener('change', handleImagePreview);
    document.getElementById('remove-image').addEventListener('click', clearImagePreview);
}

// Load cities for dropdown
async function loadCities() {
    try {
        const response = await fetch('/api/cities');
        const cities = await response.json();
        
        const citySelect = document.getElementById('city-filter');
        citySelect.innerHTML = '<option value="">選擇縣市</option>';
        
        cities.forEach(city => {
            const option = document.createElement('option');
            option.value = city;
            option.textContent = city;
            citySelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading cities:', error);
    }
}

// Load districts for selected city
async function loadDistricts(city) {
    try {
        const response = await fetch(`/api/districts/${encodeURIComponent(city)}`);
        const districts = await response.json();
        
        const districtSelect = document.getElementById('district-filter');
        districtSelect.innerHTML = '<option value="">選擇地區</option>';
        
        districts.forEach(district => {
            const option = document.createElement('option');
            option.value = district;
            option.textContent = district;
            districtSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading districts:', error);
    }
}

// Load building types
async function loadBuildingTypes() {
    try {
        const response = await fetch('/api/listings/building-types');
        const types = await response.json();
        
        const typeSelect = document.getElementById('building-type-filter');
        typeSelect.innerHTML = '<option value="">所有類型</option>';
        
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            typeSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading building types:', error);
    }
}

// Load layouts
async function loadLayouts() {
    try {
        const response = await fetch('/api/layouts');
        const layouts = await response.json();
        
        const layoutSelect = document.getElementById('layout-filter');
        layoutSelect.innerHTML = '<option value="">所有格局</option>';
        
        layouts.forEach(layout => {
            const option = document.createElement('option');
            option.value = layout;
            option.textContent = layout;
            layoutSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading layouts:', error);
    }
}

// Toggle between search modes
function toggleSearchMode() {
    const traditionalMode = document.getElementById('traditional-mode').checked;
    const traditionalSearch = document.getElementById('traditional-search');
    const smartSearch = document.getElementById('smart-search');
    
    if (traditionalMode) {
        traditionalSearch.classList.remove('d-none');
        smartSearch.classList.add('d-none');
    } else {
        traditionalSearch.classList.add('d-none');
        smartSearch.classList.remove('d-none');
    }
}

// Perform traditional search
function performSearch() {
    currentFilters.keyword = document.getElementById('keyword-search').value;
    currentFilters.search_mode = 'traditional';
    currentPage = 1;
    loadListings();
}

// Perform smart search (NLP + Vector similarity)
async function performSmartSearch() {
    const smartQuery = document.getElementById('smart-query').value;
    const referenceImage = document.getElementById('reference-image').files[0];
    const alpha = document.getElementById('alpha-slider').value / 100; // Convert to 0-1 range
    const threshold = document.getElementById('threshold-slider').value / 100; // Convert to 0-1 range
    
    if (!smartQuery.trim() && !referenceImage) {
        alert('請輸入描述文字或上傳參考圖片');
        return;
    }
    
    // Show loading spinner
    showLoading();
    
    try {
        // Parse natural language query
        let residualQuery = '';
        let filterExists = false;
        console.log('Performing smart search with text query:', smartQuery);
        if (smartQuery.trim()) {
            try {
                const res = await fetch('/api/llm/parse_nl', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ query: smartQuery })
                });


                if (!res.ok) {
                    throw new Error(`Failed to parse natural language: ${res.statusText}`);
                }
                const data = await res.json();
                const parsed_filter = JSON.parse(data.output[0].content[0].text);
                residualQuery = parsed_filter.other_requests || '';
                console.log('Parsed filters:', parsed_filter);
                console.log('Residual query:', residualQuery);

                clearFilters(reload=false);
                // Apply parsed filters

                if (parsed_filter.city) {
                    console.log('Setting city filter:', parsed_filter.city);
                    const citySelect = document.getElementById('city-filter');
                    const cityOption = Array.from(citySelect.options).find(option => option.value === parsed_filter.city);
                    if (cityOption) {
                        filterExists = true;
                        citySelect.value = parsed_filter.city;
                        await loadDistricts(parsed_filter.city);
                        if (parsed_filter.district) {
                            const districtSelect = document.getElementById('district-filter');
                            const districtOption = Array.from(districtSelect.options).find(option => option.value === parsed_filter.district);
                            if (districtOption) {
                                filterExists = true;
                                districtSelect.value = parsed_filter.district;
                            }
                        }
                    }
                }

                if (parsed_filter.price_range) {
                    if (parsed_filter.price_range.min) {
                        document.getElementById('price-min').value = parsed_filter.price_range.min;
                        filterExists = true;
                    }
                    if (parsed_filter.price_range.max) {
                        document.getElementById('price-max').value = parsed_filter.price_range.max;
                        filterExists = true;
                    }
                }

                if (parsed_filter.price_range) {
                    if (parsed_filter.price_range.min) {
                        document.getElementById('price-min').value = parsed_filter.price_range.min;
                        filterExists = true;
                    }
                    if (parsed_filter.price_range.max) {
                        document.getElementById('price-max').value = parsed_filter.price_range.max;
                        filterExists = true;
                    }
                }

                if (parsed_filter.area_range) {
                    const coef = parsed_filter.area_range.unit === 'm^2' ? 0.3025 : 1.0;
                    const { min, max } = parsed_filter.area_range;
                    if (max) {
                        document.getElementById('area-max').value = max * coef;
                        filterExists = true;
                    }
                    if (min) {
                        document.getElementById('area-min').value = min * coef;
                        filterExists = true;
                    }
                }

                if (parsed_filter.property_type) {
                    const buildingTypeSelect = document.getElementById('building-type-filter');
                    const buildingTypeOption = Array.from(buildingTypeSelect.options).find(option => option.value === parsed_filter.property_type);
                    if (buildingTypeOption) {
                        filterExists = true;
                        buildingTypeSelect.value = parsed_filter.property_type;
                    }
                }

                if (parsed_filter.facilities.length > 0) {
                    const facilityCheckboxes = document.querySelectorAll('.facility-filters input[type="checkbox"]');
                    facilityCheckboxes.forEach(checkbox => {
                        if (parsed_filter.facilities.includes(checkbox.id)) {
                            checkbox.checked = true;
                            filterExists = true;
                        } else {
                            checkbox.checked = false;
                        }
                    });
                }

                if (parsed_filter.rules.length > 0) {
                    const ruleCheckboxes = document.querySelectorAll('.rule-filters input[type="checkbox"]');
                    ruleCheckboxes.forEach(checkbox => {
                        if (parsed_filter.rules.includes(checkbox.id)) {
                            checkbox.checked = true;
                            filterExists = true;
                        } else {
                            checkbox.checked = false;
                        }
                    });
                }

            } catch (err) {
                residualQuery = smartQuery;
                console.error('Failed to parse natural language:', err.message);
            }
        }

        if (!residualQuery.trim() && !referenceImage) {
            if (!filterExists) {
                alert('請輸入描述文字或上傳參考圖片');
                hideLoading();
                return;
            } else {
                console.log('No residual query, applying filters');
                applyFilters();
                return;
            }
        }

        const formData = new FormData();
        if (residualQuery.trim()) {
            formData.append('query_text', residualQuery);
        }
        if (referenceImage) {
            formData.append('query_image', referenceImage);
        }
        
        // Add weights and threshold
        formData.append('text_weight', alpha);
        formData.append('image_weight', 1 - alpha);
        formData.append('threshold', threshold);
        
        const response = await fetch('/api/smart-search', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || '搜尋失敗');
        }
        
        const data = await response.json();
        
        // Update results count
        updateResultsInfo(data.pagination.total);
        
        // Display results
        displayListings(data.listings);
        
    } catch (error) {
        console.error('Error:', error);
        showError('搜尋失敗，請稍後再試');
    } finally {
        if (!isLoading) {
            hideLoading();
        }
    }
}

// Apply filters
function applyFilters() {
    console.log(document.getElementById('city-filter').value);
    currentFilters = {
        keyword: document.getElementById('keyword-search').value,
        city: document.getElementById('city-filter').value,
        district: document.getElementById('district-filter').value,
        price_min: document.getElementById('price-min').value,
        price_max: document.getElementById('price-max').value,
        area_min: document.getElementById('area-min').value,
        area_max: document.getElementById('area-max').value,
        building_type: document.getElementById('building-type-filter').value,
        layout: document.getElementById('layout-filter').value,
        sort_by: document.getElementById('sort-by').value
    };
    
    // Add facility filters
    const facilityCheckboxes = document.querySelectorAll('.facility-filters input[type="checkbox"]');
    facilityCheckboxes.forEach(checkbox => {
        if (checkbox.checked) {
            currentFilters[checkbox.id] = 'true';
        }
    });
    
    // Add rule filters
    const ruleCheckboxes = document.querySelectorAll('.rule-filters input[type="checkbox"]');
    ruleCheckboxes.forEach(checkbox => {
        if (checkbox.checked) {
            currentFilters[checkbox.id] = 'true';
        }
    });
    
    currentPage = 1;
    loadListings();
}

// Clear all filters
function clearFilters(reload = true) {
    // Clear form inputs
    document.getElementById('keyword-search').value = '';
    document.getElementById('city-filter').value = '';
    document.getElementById('district-filter').innerHTML = '<option value="">選擇地區</option>';
    document.getElementById('price-min').value = '';
    document.getElementById('price-max').value = '';
    document.getElementById('area-min').value = '';
    document.getElementById('area-max').value = '';
    document.getElementById('building-type-filter').value = '';
    document.getElementById('layout-filter').value = '';
    document.getElementById('sort-by').value = 'updated_at_desc';
    
    // Clear checkboxes
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Reset filters and reload
    currentFilters = {};
    currentPage = 1;
    if (reload) {
        loadListings();
    }
}

// Load listings with current filters
async function loadListings() {
    console.log(isLoading ? 'Already loading...' : 'Loading listings...');
    if (isLoading) return;

    console.log('Loading listings');
    
    isLoading = true;
    showLoading();
    
    try {
        // Build query parameters
        const pageSize = document.getElementById('page-size').value || 10;
        const params = new URLSearchParams({
            page: currentPage,
            limit: pageSize,
            ...currentFilters
        });
        
        // Remove empty parameters
        for (let [key, value] of params.entries()) {
            if (!value) {
                params.delete(key);
            }
        }
        
        const response = await fetch(`/api/listings?${params.toString()}`);
        const data = await response.json();
        
        if (response.ok) {
            displayListings(data.listings);
            updatePagination(data.pagination);
            updateResultsInfo(data.pagination.total);
        } else {
            showError('載入房源時發生錯誤');
        }
    } catch (error) {
        console.error('Error loading listings:', error);
        showError('網路連線錯誤，請稍後再試');
    } finally {
        isLoading = false;
        hideLoading();
    }
}

// Display listings in grid
function displayListings(listings) {
    const grid = document.getElementById('listings-grid');
    
    if (!listings || listings.length === 0) {
        grid.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    <i class="fas fa-search"></i>
                    <h4>找不到符合條件的房源</h4>
                    <p>請嘗試調整搜尋條件或篩選器</p>
                </div>
            </div>
        `;
        return;
    }
    
    const listingCards = listings.map(listing => createListingCard(listing)).join('');
    grid.innerHTML = listingCards;
    
    // Add fade-in animation
    grid.classList.add('fade-in');
}

// Create listing card HTML
function createListingCard(listing) {
    const firstImage = listing.images && listing.images.length > 0 
        ? listing.images[0].image_url 
        : null;
    
    const facilitiesCount = listing.facilities 
        ? Object.values(listing.facilities).filter(Boolean).length 
        : 0;
    
    const rulesText = [];
    if (listing.rules) {
        if (listing.rules.cooking_allowed) rulesText.push('可開伙');
        if (listing.rules.pet_allowed) rulesText.push('可養寵物');
        if (listing.rules.short_term_allowed) rulesText.push('可短租');
    }
    
    return `
        <div class="col-lg-4 col-md-6 col-sm-12">
            <a href="/listings/${listing.id}" class="listing-card-link">
                <div class="card listing-card">
                    <div class="position-relative">
                        ${firstImage 
                            ? `<img src="${firstImage}" class="card-img-top" alt="${listing.title}">`
                            : `<div class="no-image-placeholder card-img-top">
                                 <i class="fas fa-image fa-2x"></i>
                                 <p class="mb-0 small">暫無圖片</p>
                               </div>`
                        }
                        ${listing.images && listing.images.length > 1 
                            ? `<span class="badge bg-dark position-absolute" style="top: 10px; right: 10px;">
                                 <i class="fas fa-images me-1"></i>${listing.images.length}
                               </span>`
                            : ''
                        }
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <span class="price">NT$ ${listing.price.toLocaleString()}</span>
                            <small class="text-muted">${listing.area || '?'}坪</small>
                        </div>
                        <h6 class="card-title title mb-2">${listing.title}</h6>
                        <p class="location mb-2">
                            <i class="fas fa-map-marker-alt me-1"></i>
                            ${listing.city} ${listing.district}
                        </p>
                        <div class="details mb-2">
                            <small class="text-muted">
                                ${listing.building_type || '類型未提供'} | 
                                ${listing.layout || '格局未提供'} | 
                                ${listing.floor || '樓層未提供'}
                            </small>
                        </div>
                        ${facilitiesCount > 0 
                            ? `<div class="mb-2">
                                 <small class="facility-tag">
                                   <i class="fas fa-check me-1"></i>${facilitiesCount}項設備
                                 </small>
                               </div>`
                            : ''
                        }
                        ${rulesText.length > 0 
                            ? `<div class="mb-2">
                                 ${rulesText.map(rule => `<span class="facility-tag">${rule}</span>`).join('')}
                               </div>`
                            : ''
                        }
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">
                                ${listing.available_from || '可入住日待確認'}
                            </small>
                            <span class="btn btn-sm btn-outline-orange">
                                查看詳情
                            </span>
                        </div>
                    </div>
                </div>
            </a>
        </div>
    `;
}

// Update pagination
function updatePagination(pagination) {
    const paginationElement = document.getElementById('pagination');
    
    if (pagination.pages <= 1) {
        paginationElement.innerHTML = '';
        return;
    }
    
    let paginationHTML = '';
    
    // Previous button
    if (pagination.has_prev) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="changePage(${pagination.page - 1})">
                    <i class="fas fa-chevron-left"></i>
                </a>
            </li>
        `;
    }
    
    // Page numbers
    const startPage = Math.max(1, pagination.page - 2);
    const endPage = Math.min(pagination.pages, pagination.page + 2);
    
    if (startPage > 1) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="changePage(1)">1</a>
            </li>
        `;
        if (startPage > 2) {
            paginationHTML += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <li class="page-item ${i === pagination.page ? 'active' : ''}">
                <a class="page-link" href="#" onclick="changePage(${i})">${i}</a>
            </li>
        `;
    }
    
    if (endPage < pagination.pages) {
        if (endPage < pagination.pages - 1) {
            paginationHTML += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="changePage(${pagination.pages})">${pagination.pages}</a>
            </li>
        `;
    }
    
    // Next button
    if (pagination.has_next) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="changePage(${pagination.page + 1})">
                    <i class="fas fa-chevron-right"></i>
                </a>
            </li>
        `;
    }
    
    paginationElement.innerHTML = paginationHTML;
    currentPage = pagination.page;
    totalPages = pagination.pages;
}

// Change page
function changePage(page) {
    if (page >= 1 && page <= totalPages && page !== currentPage) {
        currentPage = page;
        loadListings();
        
        // Scroll to top smoothly
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }
}

// Update results info
function updateResultsInfo(total) {
    document.getElementById('total-count').textContent = total.toLocaleString();
}

// Show loading spinner
function showLoading() {
    document.getElementById('loading-spinner').classList.remove('d-none');
    document.getElementById('listings-grid').style.opacity = '0.5';
}

// Hide loading spinner
function hideLoading() {
    document.getElementById('loading-spinner').classList.add('d-none');
    document.getElementById('listings-grid').style.opacity = '1';
}

// Show error message
function showError(message) {
    const grid = document.getElementById('listings-grid');
    grid.innerHTML = `
        <div class="col-12">
            <div class="alert alert-danger text-center" role="alert">
                <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                <h5>載入失敗</h5>
                <p>${message}</p>
                <button class="btn btn-primary" onclick="loadListings()">重新載入</button>
            </div>
        </div>
    `;
}

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('zh-TW').format(price);
}

function truncateText(text, maxLength) {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// Handle image preview
function handleImagePreview(event) {
    const file = event.target.files[0];
    const previewContainer = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const fileInfo = document.getElementById('file-info');
    
    if (file) {
        // Validate file type
        if (!file.type.startsWith('image/')) {
            alert('請選擇圖片檔案');
            event.target.value = '';
            return;
        }
        
        // Validate file size (5MB max)
        const maxSize = 5 * 1024 * 1024; // 5MB
        if (file.size > maxSize) {
            alert('圖片檔案不能超過 5MB');
            event.target.value = '';
            return;
        }
        
        // Create preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewContainer.classList.remove('d-none');
            
            // Show file info
            const sizeInKB = (file.size / 1024).toFixed(1);
            fileInfo.textContent = `檔案: ${file.name} (${sizeInKB} KB)`;
        };
        reader.readAsDataURL(file);
    } else {
        clearImagePreview();
    }
}

// Clear image preview
function clearImagePreview() {
    const previewContainer = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const fileInput = document.getElementById('reference-image');
    const fileInfo = document.getElementById('file-info');
    
    previewContainer.classList.add('d-none');
    previewImg.src = '';
    fileInput.value = '';
    fileInfo.textContent = '';
}

// Update slider values
function updateSliderValues() {
    const alphaSlider = document.getElementById('alpha-slider');
    const alphaValue = document.getElementById('alpha-value');
    const thresholdSlider = document.getElementById('threshold-slider');
    const thresholdValue = document.getElementById('threshold-value');
    
    alphaSlider.addEventListener('input', function() {
        alphaValue.textContent = `${this.value}% 文字`;
    });
    
    thresholdSlider.addEventListener('input', function() {
        thresholdValue.textContent = `${this.value}% 相似度`;
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeFilters();
    loadListings();
    updateSliderValues();
});

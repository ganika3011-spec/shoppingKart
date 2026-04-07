// ========================================
// MODERN SHOPPING CART UI - JavaScript
// ========================================

document.addEventListener('DOMContentLoaded', function() {
  
  // ========== SMOOTH SCROLL & STICKY NAVBAR ==========
  const header = document.querySelector('.header-top');
  
  window.addEventListener('scroll', function() {
    if (window.scrollY > 50) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }
  });

  // ========== SMOOTH SCROLL FOR ANCHOR LINKS ==========
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && document.querySelector(href)) {
        e.preventDefault();
        document.querySelector(href)?.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // ========== TOAST NOTIFICATIONS ==========
  function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show`;
    toast.setAttribute('role', 'alert');
    toast.style.cssText = `
      min-width: 300px;
      margin-bottom: 10px;
      animation: slideInRight 300ms ease-out;
    `;
    
    const icons = {
      'success': '✓',
      'danger': '✕',
      'warning': '⚠',
      'info': 'ℹ'
    };
    
    toast.innerHTML = `
      <strong>${icons[type]}</strong> ${message}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    `;
    
    container.appendChild(toast);
    
    // Auto-dismiss after duration
    setTimeout(() => {
      toast.remove();
    }, duration);
  }

  function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
    `;
    document.body.appendChild(container);
    return container;
  }

  // ========== ADD TO CART FUNCTIONALITY ==========
  document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const productId = this.dataset.productId;
      const originalText = this.innerHTML;
      
      // Show loading state
      this.innerHTML = '<i class="fas fa-spinner fa-spin mr-1"></i> Adding...';
      this.disabled = true;
      
      // Simulate adding to cart (replace with actual API call)
      setTimeout(() => {
        this.innerHTML = originalText;
        this.disabled = false;
        showToast('Product added to cart!', 'success');
        
        // Animate cart badge
        const cartBadge = document.querySelector('.cart-badge');
        if (cartBadge) {
          cartBadge.style.animation = 'pulse 400ms ease-out';
        }
      }, 500);
    });
  });

  // ========== QUANTITY CONTROLS ==========
  document.querySelectorAll('.qty-decrease').forEach(btn => {
    btn.addEventListener('click', function() {
      const input = this.nextElementSibling;
      if (input && input.value > 1) {
        input.value--;
        updateCartTotal();
      }
    });
  });

  document.querySelectorAll('.qty-increase').forEach(btn => {
    btn.addEventListener('click', function() {
      const input = this.previousElementSibling;
      if (input) {
        input.value++;
        updateCartTotal();
      }
    });
  });

  // ========== CART TOTAL UPDATE ==========
  function updateCartTotal() {
    const items = document.querySelectorAll('.cart-item');
    let total = 0;
    
    items.forEach(item => {
      const priceText = item.querySelector('.item-price').textContent;
      const qty = item.querySelector('.item-qty').value;
      const price = parseFloat(priceText.replace('$', ''));
      total += price * qty;
    });
    
    const totalElement = document.querySelector('.cart-total-amount');
    if (totalElement) {
      totalElement.textContent = '$' + total.toFixed(2);
    }
  }

  // ========== FORM VALIDATION ==========
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
        showToast('Please fill all required fields', 'warning');
      }
      form.classList.add('was-validated');
    });
  });

  // ========== CATEGORY FILTER ==========
  document.querySelectorAll('.category-filter').forEach(link => {
    link.addEventListener('click', function(e) {
      document.querySelectorAll('.category-filter').forEach(l => {
        l.classList.remove('active');
      });
      this.classList.add('active');
    });
  });

  // ========== PRICE RANGE SLIDER ==========
  const priceInputs = document.querySelectorAll('.price-range');
  if (priceInputs.length > 0) {
    priceInputs.forEach(input => {
      input.addEventListener('change', function() {
        updatePriceDisplay();
      });
    });
  }

  function updatePriceDisplay() {
    const minPrice = document.querySelector('.price-min')?.value || 0;
    const maxPrice = document.querySelector('.price-max')?.value || 1000;
    const display = document.querySelector('.price-display');
    if (display) {
      display.textContent = `$${minPrice} - $${maxPrice}`;
    }
  }

  // ========== DROPDOWN ANIMATIONS ==========
  document.querySelectorAll('.dropdown').forEach(dropdown => {
    dropdown.addEventListener('shown.bs.dropdown', function() {
      this.querySelector('.dropdown-menu')?.style.setProperty('animation', 'slideDown 300ms ease-out');
    });
  });

  // ========== STAR RATING INTERACTIVE ==========
  document.querySelectorAll('.rating-interactive').forEach(ratingContainer => {
    const stars = ratingContainer.querySelectorAll('.star-btn');
    
    stars.forEach((star, index) => {
      star.addEventListener('mouseover', () => {
        stars.forEach((s, i) => {
          if (i <= index) {
            s.classList.add('text-warning');
            s.style.transform = 'scale(1.1)';
          } else {
            s.classList.remove('text-warning');
            s.style.transform = 'scale(1)';
          }
        });
      });

      star.addEventListener('click', () => {
        const rating = index + 1;
        const ratingInput = ratingContainer.querySelector('input[name="rating"]');
        if (ratingInput) {
          ratingInput.value = rating;
          showToast(`You rated this product ${rating} stars!`, 'success');
        }
      });
    });

    ratingContainer.addEventListener('mouseleave', () => {
      stars.forEach(s => {
        s.classList.remove('text-warning');
        s.style.transform = 'scale(1)';
      });
    });
  });

  // ========== SEARCH SUGGESTIONS ==========
  const searchInput = document.querySelector('input[name="keyword"]');
  if (searchInput) {
    searchInput.addEventListener('focus', function() {
      this.style.boxShadow = '0 0 0 4px rgba(0,123,255,0.25)';
    });

    searchInput.addEventListener('blur', function() {
      this.style.boxShadow = 'none';
    });

    searchInput.addEventListener('input', function() {
      // Add search suggestions logic here
    });
  }

  // ========== PRODUCT IMAGE ZOOM ==========
  document.querySelectorAll('.product-detail-image').forEach(img => {
    img.addEventListener('mouseover', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const xPercent = (x / rect.width) * 100;
      const yPercent = (y / rect.height) * 100;
      
      this.style.transformOrigin = `${xPercent}% ${yPercent}%`;
      this.style.transform = 'scale(1.5)';
    });

    img.addEventListener('mouseleave', function() {
      this.style.transform = 'scale(1)';
    });
  });

  // ========== MODAL HELPER ==========
  window.showModal = function(title, message, type = 'info') {
    const modal = document.createElement('div');
    modal.innerHTML = `
      <div class="modal fade" role="dialog" style="display: block;">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">${title}</h5>
              <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <p>${message}</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            </div>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
  };

  // ========== LAZY LOADING IMAGES ==========
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src || img.src;
          img.classList.add('loaded');
          observer.unobserve(img);
        }
      });
    });

    document.querySelectorAll('img[data-src]').forEach(img => {
      imageObserver.observe(img);
    });
  }

  // ========== SIDE-BY-SIDE COMPARISON ==========
  window.compareProducts = function(product1Id, product2Id) {
    console.log(`Comparing products: ${product1Id} and ${product2Id}`);
    showToast('Comparison feature coming soon!', 'info');
  };

  // ========== WISHLIST TOGGLE ==========
  document.querySelectorAll('.wishlist-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      this.classList.toggle('active');
      const isActive = this.classList.contains('active');
      showToast(
        isActive ? 'Added to wishlist!' : 'Removed from wishlist!',
        isActive ? 'success' : 'info'
      );
    });
  });

  // ========== SCROLL TO TOP BUTTON ==========
  const scrollTopBtn = document.querySelector('.scroll-top-btn');
  if (scrollTopBtn) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        scrollTopBtn.style.display = 'block';
      } else {
        scrollTopBtn.style.display = 'none';
      }
    });

    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ========== NAVBAR DROPDOWN KEYBOARD NAV ==========
  document.querySelectorAll('[role="menuitem"]').forEach(item => {
    item.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        this.click();
      }
    });
  });

  console.log('✓ Modern shopping cart UI initialized successfully!');
});

// ========== GLOBAL UTILITY FUNCTIONS ==========
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

// ========== ANIMATION UTILITIES ==========
function animateValue(element, start, end, duration) {
  const range = end - start;
  const increment = end > start ? 1 : -1;
  const stepTime = Math.abs(Math.floor(duration / range));
  let current = start;

  const timer = setInterval(() => {
    current += increment;
    element.textContent = current;
    if (current === end) clearInterval(timer);
  }, stepTime);
}

// ========== KEYBOARD SHORTCUTS ==========
document.addEventListener('keydown', function(e) {
  // Ctrl/Cmd + / for search
  if ((e.ctrlKey || e.metaKey) && e.key === '/') {
    e.preventDefault();
    document.querySelector('input[name="keyword"]')?.focus();
  }
  // Escape to close modals
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal.show').forEach(m => {
      const modalInstance = bootstrap?.Modal?.getOrCreateInstance(m);
      modalInstance?.hide();
    });
  }
});

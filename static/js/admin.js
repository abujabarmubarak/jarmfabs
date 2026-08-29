/**
 * JarmFabs Technologies — Admin Dashboard Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Image Preview on File Input Selection
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach(input => {
    input.addEventListener('change', function(e) {
      const file = this.files[0];
      if (file) {
        // Find existing or create preview container
        let previewWrap = this.parentElement.querySelector('.upload-preview');
        if (!previewWrap) {
          previewWrap = document.createElement('div');
          previewWrap.className = 'upload-preview';
          this.parentElement.appendChild(previewWrap);
        }

        const reader = new FileReader();
        reader.onload = function(event) {
          previewWrap.innerHTML = `<img src="${event.target.result}" alt="Preview" />`;
          previewWrap.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  });

  // 2. Delete Confirmation
  const deleteForms = document.querySelectorAll('form.delete-form, form[action*="delete"]');
  deleteForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      if (!confirm('Are you sure you want to permanently delete this item? This action cannot be undone.')) {
        e.preventDefault();
      }
    });
  });
});

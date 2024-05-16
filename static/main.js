document.addEventListener('DOMContentLoaded', function() {
    const typeButtons = document.querySelectorAll('.type-btn');
    const typeInput = document.getElementById('type-input');
  
    typeButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        event.preventDefault();
        typeButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
        typeInput.value = this.getAttribute('data-value');
      });
    });
  });
  
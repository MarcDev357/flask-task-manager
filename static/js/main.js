// All custom JS for Task Manager

document.addEventListener("DOMContentLoaded", function () {
    // Dark Mode Toggle
    const darkToggle = document.getElementById("darkToggle");
    const body = document.body;
  
    if (darkToggle) {
      darkToggle.addEventListener("click", () => {
        body.classList.toggle("bg-dark");
        body.classList.toggle("text-light");
  
        const elements = document.querySelectorAll(".card, .list-group-item, .navbar");
        elements.forEach(el => {
          el.classList.toggle("bg-dark");
          el.classList.toggle("text-light");
        });
      });
    }
  
    // Auto-dismiss alerts after 3 seconds
    const alert = document.querySelector('.alert');
    if (alert) {
      setTimeout(() => {
        alert.classList.remove('show');
        alert.classList.add('fade');
      }, 3000);
    }
  });
  
document.addEventListener('click', (event) => {
  const button = event.target.closest('.toggle-visibility');
  if (!button) return;

  const targetId = button.getAttribute('data-target');
  if (!targetId) return;

  const input = document.getElementById(targetId);
  if (!input) return;

  const isPassword = input.getAttribute('type') === 'password';
  input.setAttribute('type', isPassword ? 'text' : 'password');
  button.setAttribute('aria-pressed', isPassword ? 'true' : 'false');
  button.setAttribute('data-visible', isPassword ? 'true' : 'false');
});

document.addEventListener('DOMContentLoaded', () => {
  const revealElements = document.querySelectorAll('.reveal');
  if (!revealElements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15,
  });

  revealElements.forEach((el) => observer.observe(el));
});

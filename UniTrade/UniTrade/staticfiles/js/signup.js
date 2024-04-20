// Example 1: Add validation for email format
const emailInput = document.getElementById('id_email');

emailInput.addEventListener('blur', function() {
  const email = this.value;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    alert('Please enter a valid email address.');
  }
});

// Example 2: Show/hide password on checkbox click
const passwordInput1 = document.getElementById('id_password1');
const passwordInput2 = document.getElementById('id_password2');

const showPasswordCheckbox = document.getElementById('show_password');

showPasswordCheckbox.addEventListener('click', function() {
  if (this.checked) {
    passwordInput1.type = 'text';
    passwordInput2.type = 'text';

  } else {
    passwordInput1.type = 'password';
    passwordInput2.type = 'password';
  }
});

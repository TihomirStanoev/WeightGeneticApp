
const form = document.querySelector('#login-form');
const usernameField = document.querySelector('#login-input');
const passwordField = document.querySelector('#password-input');

form.addEventListener('submit', async function (event) {
    event.preventDefault();

    const response = await fetch('/api/token/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: usernameField.value, password: passwordField.value})
    });
    const data = await response.json();
    const accessToken = data.access;
    const refreshToken = data.refresh;
    const details = data.detail;

    if (accessToken && refreshToken) {
        localStorage.setItem('access', accessToken);
        localStorage.setItem('refresh', refreshToken);
    }
    if (details) {
        alert(details);
    }



});


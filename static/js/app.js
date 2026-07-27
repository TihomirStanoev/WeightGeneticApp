async function loadProfiles() {
    const accessToken = localStorage.getItem('access');
    const profiles = await fetch(
        '/api/master-data/profiles/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        }
    );

    const data = await profiles.json();
    console.log(data);
}

const but = document.querySelector('#but');


but.addEventListener('click', loadProfiles)


const form = document.querySelector('#login-form');
const usernameField = document.querySelector('#login-input');
const passwordField = document.querySelector('#password-input');
const errorDiv = document.querySelector('#error')

form.addEventListener('submit', async function (event) {
    event.preventDefault();

    const response = await fetch('/api/token/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username: usernameField.value, password: passwordField.value})
    });

    const data = await response.json();

    errorDiv.textContent = ''

    if (!response.ok) {
        let error = ''
        for (const [k, v] of Object.entries(data)) {
             error += `${k}: ${v}\n`
        }
        return errorDiv.textContent = error
    }

    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);

});

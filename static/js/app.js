const form = document.querySelector('#login-form');
const usernameField = document.querySelector('#login-input');
const passwordField = document.querySelector('#password-input');
const but = document.querySelector('#but');
const profilesContainer = document.querySelector('#profiles');

const errorDiv = document.querySelector('#error')

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    errorDiv.textContent = '';
    try {
        await login(usernameField.value, passwordField.value);
    } catch (err) {
        errorDiv.textContent = err.message;
    }
});


but.addEventListener('click', async function () {
    profilesContainer.textContent = '';
    try {
        const profiles = await getProfiles();

        for (let profile of profiles) {
            const li = document.createElement('li');
            const b = document.createElement('b');
            b.textContent = profile.code;
            li.appendChild(b);
            li.append(` - ${profile.description}: ${profile.theoretical_gpm} gr/m`);
            profilesContainer.appendChild(li);
        }

    } catch (err) {
        errorDiv.textContent = err.message;
    }
});
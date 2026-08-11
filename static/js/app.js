const form = document.querySelector('#login-form');
const usernameField = document.querySelector('#login-input');
const passwordField = document.querySelector('#password-input');
const but = document.querySelector('#but');
const profilesContainer = document.querySelector('#profiles');
const errorDiv = document.querySelector('#error');
const workpiecesUi = document.querySelector('#workpieces');
const referencesUi = document.querySelector('#references');

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    errorDiv.textContent = '';
    try {
        await login(usernameField.value, passwordField.value);
    } catch (err) {
        errorDiv.textContent = err.message;
    }
});

function renderReferences(references) {
    referencesUi.textContent = '';

    for (let reference of references) {
        const referenceLi = document.createElement('li');
        referenceLi.textContent = `${reference.material} ${reference.description}`;
        referencesUi.appendChild(referenceLi);
    }
}

function renderWorkpieces(workpieces, profileCode) {
    workpiecesUi.textContent = '';

    for (let workpiece of workpieces) {
        const workpieceLi = document.createElement('li');
        const b = document.createElement('b');
        b.textContent = workpiece.material;
        workpieceLi.appendChild(b);
        workpieceLi.append(` ${workpiece.description}`);
        workpiecesUi.appendChild(workpieceLi);

        b.addEventListener('click', async function() {
            try {
                const references = await getReference(profileCode, workpiece.material);
                renderReferences(references);
            } catch (err) {
                errorDiv.textContent = err.message;
            }
        })
    }
}


function renderProfiles(profiles) {
    profilesContainer.textContent = '';

    for (let profile of profiles) {
        const li = document.createElement('li');
        const b = document.createElement('b');
        b.textContent = profile.code;

        li.appendChild(b);
        li.append(` - ${profile.description}: ${profile.theoretical_gpm} gr/m`);
        profilesContainer.appendChild(li);

        b.addEventListener('click', async function () {
            try {
                const workpieces = await getWorkpieces(profile.code);
                renderWorkpieces(workpieces, profile.code);
            } catch (err) {
                errorDiv.textContent = err.message;
            }
        });
    }
}


but.addEventListener('click', async function () {
    try {
        const profiles = await getProfiles();
        renderProfiles(profiles);

    } catch (err) {
        errorDiv.textContent = err.message;
    }

});
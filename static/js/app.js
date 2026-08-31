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


async function loadAndRender(fetcher, renderer) {
    try {
        const data = await fetcher();
        renderer(data);
    } catch (err) {
        errorDiv.textContent = err.message;
    }
}



function renderReferences(references) {
    referencesUi.textContent = '';
    for (let reference of references) {
        const referenceLi = document.createElement('li');
        const referenceB = document.createElement('b');
        const customerNumber = document.createElement('span');
        const referenceDescription = document.createElement('span');
        const referenceTheoreticalWeight = document.createElement('span');
        const referenceDiv = document.createElement('div');

        referenceDiv.classList.add('ref-meta');
        customerNumber.classList.add('tag');
        referenceDescription.classList.add('ref-desc');
        referenceTheoreticalWeight.classList.add('tag');


        referenceB.textContent = reference.material;
        referenceDescription.textContent = reference.description;


        customerNumber.textContent = reference.customer_number || 'N/a';
        referenceTheoreticalWeight.textContent = `${reference.theoretical_weight} gr.`;

        referenceDiv.appendChild(customerNumber);
        referenceDiv.appendChild(referenceTheoreticalWeight);

        referenceLi.appendChild(referenceB);
        referenceLi.appendChild(referenceDescription);
        referenceLi.appendChild(referenceDiv);


        referencesUi.appendChild(referenceLi);
    }
}

function renderWorkpieces(workpieces, profileCode) {
    workpiecesUi.textContent = '';
    referencesUi.textContent = '';

    for (let workpiece of workpieces) {
        const workpieceLi = document.createElement('li');
        const b = document.createElement('b');
        b.textContent = workpiece.material;
        workpieceLi.appendChild(b);
        workpieceLi.append(` ${workpiece.description}`);
        workpiecesUi.appendChild(workpieceLi);

        b.addEventListener('click', async function() {
            await loadAndRender(
                () => getReference(profileCode, workpiece.material),
                renderReferences
            );
        });
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
            await loadAndRender(
                () => getWorkpieces(profile.code),
                (workpieces) => renderWorkpieces(workpieces, profile.code)
            );
        });
    }
}


but.addEventListener('click', async function () {
    await loadAndRender(getProfiles, renderProfiles);
});
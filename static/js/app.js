const form = document.querySelector('#login-form');
const referenceForm = document.querySelector('#reference-form');
const usernameField = document.querySelector('#login-input');
const passwordField = document.querySelector('#password-input');
const but = document.querySelector('#but');
const profilesContainer = document.querySelector('#profiles');
const errorDiv = document.querySelector('#error');
const workpiecesUi = document.querySelector('#workpieces');
const referencesUi = document.querySelector('#references');
let selectedProfileCode = null;
let selectedWorkpieceMaterial = null;

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    errorDiv.textContent = '';
    try {
        await login(usernameField.value, passwordField.value);
    } catch (err) {
        errorDiv.textContent = err.message;
    }
});


referenceForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    errorDiv.textContent = '';

    const referenceMaterial = document.querySelector('#reference-material').value;
    const referenceCustomerNumber = document.querySelector('#reference-customer-number').value;
    const referenceDescription = document.querySelector('#reference-description').value;
    const referenceTheoreticalWeight = document.querySelector('#reference-theoretical-weight').value;

    const payload = {
        material: referenceMaterial,
        customer_number: referenceCustomerNumber,
        description: referenceDescription,
        theoretical_weight: referenceTheoreticalWeight,
    };

    try {
        await createReference(selectedProfileCode, selectedWorkpieceMaterial, payload);
        await loadAndRender(
        () => getReference(selectedProfileCode, selectedWorkpieceMaterial),
        renderReferences);
        this.reset();

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
    selectedProfileCode = null;
    selectedWorkpieceMaterial = null;
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
            selectedProfileCode = profileCode;
            selectedWorkpieceMaterial = workpiece.material;

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
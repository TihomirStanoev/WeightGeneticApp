function errorMessages(data) {
    let message = '';
    for (const [k, v] of Object.entries(data)) {
         message += `${k}: ${v}\n`
    }
    return message;
}


async function login(username, password) {
    const response = await fetch('/api/token/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, password})
    });
    const data = await response.json();


    if (!response.ok) {
        throw new Error(errorMessages(data));
    }


    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);
}


async function getProfiles() {
    const accessToken = localStorage.getItem('access');
    const response = await fetch(
        '/api/master-data/profiles/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        }
    );

    const profiles = await response.json();

    if (!response.ok) {
        throw new Error(errorMessages(profiles));
    }

    return profiles;
}

async function getWorkpieces(profileCode) {
    const accessToken = localStorage.getItem('access');
    const response = await fetch(
        `/api/master-data/profiles/${profileCode}/workpieces/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        }
    );

    const workpieces = await response.json();

    if (!response.ok) {
        throw new Error(errorMessages(workpieces));
    }

    return workpieces;
}
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


async function getData(urlInput) {
    const accessToken = localStorage.getItem('access');
    const response = await fetch(
        urlInput, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        }
    );

    const data = await response.json();
    if (!response.ok) {
        throw new Error(errorMessages(data));
    }

    return data;
}


async function getProfiles () {
    return getData(`/api/master-data/profiles/`)
}

async function getWorkpieces(profileCode) {
    return getData(`/api/master-data/profiles/${profileCode}/workpieces/`)
}
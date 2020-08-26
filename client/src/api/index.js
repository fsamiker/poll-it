const API_URL = 'http://127.0.0.1:5000/api'

export function authenticate (credentials) {
    return fetch(`${API_URL}/auth/tokens/`, {
        method: 'POST',
        headers: { 'Authorization': 'Basic ' + btoa(credentials.username+':'+ credentials.password) }
    })
}

export function unauthenticate (auth_header) {
    return fetch(`${API_URL}/auth/tokens/`, {
        method: 'DELETE',
        headers: auth_header
    })
}

export function fetchPolls(user_id=null) {
    let url = `${API_URL}/polls/`
    if (user_id) {
        url = url + `?user_id=${user_id}`
    }
    return fetch(url, {
        method: 'GET'
    })
}

export function fetchPoll(id) {
    return fetch(`${API_URL}/polls/${id}/`, {
        method: 'GET'
    })
}

export function createPoll(auth_header, pollData) {
    return fetch(`${API_URL}/polls/`, {
        method: 'POST',
        headers: auth_header,
        body: JSON.stringify(pollData)
    })
}

export function deletePoll(auth_header, id) {
    return fetch(`${API_URL}/polls/${id}/`, {
        method: 'DELETE',
        headers: auth_header
    })
}

export function fetchUser(id) {
    return fetch(`${API_URL}/users/${id}/`, {
        method: 'GET',
    })
}

export function createUser(userData) {
    return fetch(`${API_URL}/users/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
}

export function updateUser(id, userData) {
    return fetch(`${API_URL}/users/${id}/`, {
        method: 'PUT',
        body: JSON.stringify(userData)
    })
}

export function voteAsGuest(option_id) {
    return fetch(`${API_URL}/vote/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        mode: 'cors',
        body: JSON.stringify({option_id: option_id})
    })
}

export function voteAsUser(auth_header, option_id) {
    return fetch(`${API_URL}/users/vote/`, {
        method: 'POST',
        headers: auth_header,
        mode: "cors",
        body: JSON.stringify({option_id: option_id})
    })
}

export function fetchUserVotedPolls(auth_header, id) {
    return fetch(`${API_URL}/users/voted/${id}/`, {
        method: 'GET',
        headers: auth_header
    })
}
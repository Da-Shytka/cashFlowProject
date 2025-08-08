const API_BASE = 'http://127.0.0.1:8000/api';

export async function apiRequest(endpoint, method = 'GET', body = null) {
  const options = {
    method,
    headers: {},
  };

  if (body) {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(body);
  }

  
  const response = await fetch(`${API_BASE}/${endpoint}`, options);
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Ошибка ${response.status}: ${errorText}`);
  }

  if (response.status === 204) {
    return null;
  }

  return await response.json();
}

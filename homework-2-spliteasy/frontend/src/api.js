const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {headers:{'Content-Type':'application/json'}, ...options});
  if (!response.ok) throw new Error((await response.json()).detail || 'Request failed');
  return response.json();
}
export const api = {
  people: () => request('/people'),
  addPerson: name => request('/people', {method:'POST', body:JSON.stringify({name})}),
  expenses: () => request('/expenses'),
  addExpense: data => request('/expenses', {method:'POST', body:JSON.stringify(data)}),
  summary: () => request('/summary'),
};
export { API_URL };


import './style.css';
import { api } from './api.js';

document.querySelector('#app').innerHTML = `<main><header><p class="eyebrow">SHARED EXPENSES</p><h1>SplitEasy</h1><p>Record a group expense and see who should pay whom.</p></header><div id="error"></div><section class="grid"><article><h2>Add person</h2><form id="person-form"><input name="name" placeholder="Name" required><button>Add</button></form><div id="people"></div></article><article><h2>Add expense</h2><form id="expense-form"><input name="description" placeholder="Description" required><input name="amount" type="number" min="0.01" step="0.01" placeholder="Amount" required><label>Payer<select name="payer" required></select></label><fieldset><legend>Participants</legend><div id="participants"></div></fieldset><button>Add expense</button></form></article></section><section class="grid"><article><h2>Balances</h2><div id="balances"></div><h3>Suggested payments</h3><div id="settlements"></div></article><article><h2>Expenses</h2><div id="expenses"></div></article></section></main>`;

const money = n => new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(n);
function showError(error) { document.querySelector('#error').textContent = error.message; }
async function render() {
  const [people, expenses, summary] = await Promise.all([api.people(), api.expenses(), api.summary()]);
  document.querySelector('#people').innerHTML = people.map(p=>`<span class="chip">${p.name}</span>`).join('') || '<p>No people yet.</p>';
  document.querySelector('[name=payer]').innerHTML = people.map(p=>`<option value="${p.id}">${p.name}</option>`).join('');
  document.querySelector('#participants').innerHTML = people.map(p=>`<label><input type="checkbox" name="participant" value="${p.id}" checked> ${p.name}</label>`).join('');
  document.querySelector('#expenses').innerHTML = expenses.map(e=>`<div class="row"><b>${e.description}</b><span>${e.payer.name} paid ${money(e.amount)}</span></div>`).join('') || '<p>No expenses yet.</p>';
  document.querySelector('#balances').innerHTML = summary.balances.map(b=>`<div class="row"><span>${b.name}</span><b class="${b.balance<0?'negative':'positive'}">${money(b.balance)}</b></div>`).join('') || '<p>No balances yet.</p>';
  document.querySelector('#settlements').innerHTML = summary.settlements.map(s=>`<p>${s.from_name} pays ${s.to_name} <b>${money(s.amount)}</b></p>`).join('') || '<p>Everyone is settled.</p>';
}
document.querySelector('#person-form').addEventListener('submit', async e=>{e.preventDefault();try{await api.addPerson(new FormData(e.target).get('name'));e.target.reset();await render();}catch(err){showError(err)}});
document.querySelector('#expense-form').addEventListener('submit', async e=>{e.preventDefault();const data=new FormData(e.target);try{await api.addExpense({description:data.get('description'),amount:Number(data.get('amount')),payer_id:Number(data.get('payer')),participant_ids:data.getAll('participant').map(Number)});e.target.reset();await render();}catch(err){showError(err)}});
render().catch(showError);


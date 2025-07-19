let sayingsData = [];
let deleteSayingId = null;
let editSayingId = null;

async function fetchSayings() {
  const loading = document.getElementById('loading');
  const error = document.getElementById('error');
  const list = document.getElementById('sayings-list');
  loading.style.display = '';
  error.classList.add('d-none');
  list.innerHTML = '';
  try {
    const resp = await fetch('/sayings');
    if (!resp.ok) throw new Error('Failed to fetch sayings');
    sayingsData = await resp.json();
    renderSayings();
  } catch (err) {
    error.textContent = err.message;
    error.classList.remove('d-none');
  } finally {
    loading.style.display = 'none';
  }
}

function renderSayings() {
  const list = document.getElementById('sayings-list');
  list.innerHTML = '';
  if (sayingsData.length === 0) {
    list.innerHTML = '<div class="alert alert-secondary">No sayings found.</div>';
    return;
  }
  sayingsData.forEach(saying => {
    const card = document.createElement('div');
    card.className = 'card mb-3 saying-card';
    card.dataset.sayingId = saying.id;

    // Actions (edit, delete)
    const actions = document.createElement('div');
    actions.className = 'saying-actions';
    // Edit button
    const editBtn = document.createElement('button');
    editBtn.title = 'Edit';
    editBtn.innerHTML = `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536M9 13l6.536-6.536a2 2 0 112.828 2.828L11.828 15.828a2 2 0 01-2.828 0L9 13zm-6 6h6v-2a2 2 0 012-2h2a2 2 0 012 2v2h6"/></svg>`;
    editBtn.onclick = () => startEditSaying(saying.id);
    actions.appendChild(editBtn);
    // Delete button
    const deleteBtn = document.createElement('button');
    deleteBtn.title = 'Delete';
    deleteBtn.innerHTML = `<svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6M1 7h22M8 7V5a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>`;
    deleteBtn.onclick = () => showDeleteModal(saying.id);
    actions.appendChild(deleteBtn);

    card.appendChild(actions);

    if (editSayingId === saying.id) {
      // Inline edit mode
      const editFields = document.createElement('div');
      editFields.className = 'edit-fields';
      editFields.innerHTML = `
        <input type="text" class="form-control mb-2" id="editSummary" value="${saying.summary}">
        <textarea class="form-control mb-2" id="editDescription" rows="2">${saying.description || ''}</textarea>
        <div class="d-flex gap-2">
          <button class="btn btn-primary btn-sm" id="saveEditBtn">Save</button>
          <button class="btn btn-secondary btn-sm" id="cancelEditBtn">Cancel</button>
        </div>
      `;
      card.appendChild(editFields);
      setTimeout(() => {
        document.getElementById('saveEditBtn').onclick = () => saveEditSaying(saying.id);
        document.getElementById('cancelEditBtn').onclick = () => cancelEditSaying();
      }, 0);
    } else {
      const cardBody = document.createElement('div');
      cardBody.className = 'card-body';
      cardBody.innerHTML = `
        <h5 class="card-title">${saying.summary}</h5>
        <p class="card-text">${saying.description || ''}</p>
        <small class="text-muted">Created: ${saying.ts_created ? new Date(saying.ts_created).toLocaleString() : ''}</small>
      `;
      card.appendChild(cardBody);
    }
    list.appendChild(card);
  });
}

function showDeleteModal(id) {
  console.log("Showing delete modal for saying id: ", id);
  deleteSayingId = id;
  const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
  modal.show();
}

document.getElementById('confirmDeleteBtn').onclick = async function() {
  if (!deleteSayingId) return;
  try {
    const resp = await fetch(`/saying/${deleteSayingId}`, { method: 'DELETE' });
    if (!resp.ok) throw new Error('Failed to delete saying');
    sayingsData = sayingsData.filter(s => s.id !== deleteSayingId);
    renderSayings();
  } catch (err) {
    alert(err.message);
  } finally {
    deleteSayingId = null;
    bootstrap.Modal.getInstance(document.getElementById('deleteModal')).hide();
  }
};

function startEditSaying(id) {
  console.log("Showing edit modal for saying id: ", id);
  editSayingId = id;
  renderSayings();
}
function cancelEditSaying() {
  editSayingId = null;
  renderSayings();
}
async function saveEditSaying(id) {
  const card = document.querySelector(`.saying-card[data-saying-id='${id}']`);
  const summary = card.querySelector('#editSummary').value.trim();
  const description = card.querySelector('#editDescription').value.trim();
  if (!summary) {
    alert('Summary is required.');
    return;
  }
  try {
    const resp = await fetch(`/saying/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ summary, description })
    });
    if (!resp.ok) throw new Error('Failed to update saying');
    const updated = await resp.json();
    sayingsData = sayingsData.map(s => s.id === id ? updated : s);
    editSayingId = null;
    renderSayings();
  } catch (err) {
    alert(err.message);
  }
}

document.getElementById('addSayingForm').onsubmit = async function(e) {
  e.preventDefault();
  const summary = document.getElementById('addSummary').value.trim();
  const description = document.getElementById('addDescription').value.trim();
  if (!summary) {
    alert('Summary is required.');
    return;
  }
  try {
    const resp = await fetch('/sayings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ summary, description })
    });
    if (!resp.ok) throw new Error('Failed to add saying');
    const newSaying = await resp.json();
    sayingsData.unshift(newSaying);
    renderSayings();
    bootstrap.Modal.getInstance(document.getElementById('addSayingModal')).hide();
    document.getElementById('addSayingForm').reset();
  } catch (err) {
    alert(err.message);
  }
};

window.addEventListener('DOMContentLoaded', fetchSayings); 
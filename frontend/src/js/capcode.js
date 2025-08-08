import { apiRequest } from '../../api.js';

const endpoints = {
  status: 'status',
  type: 'type',
  category: 'category',
  subcategory: 'subcategory',
};

document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('entitySelect');
  select.addEventListener('change', () => {
    renderAdminSection(select.value);
  });

  renderAdminSection(select.value);
});

async function renderAdminSection(entity) {
  const formContainer = document.getElementById('entityFormContainer');
  const listContainer = document.getElementById('entityListContainer');
  formContainer.innerHTML = '';
  listContainer.innerHTML = '';

  const data = await apiRequest(`${endpoints[entity]}/getlist`);
  renderForm(entity, formContainer);
  renderList(entity, data, listContainer);
}

function renderForm(entity, container) {
    let formHtml = `
    <form class="entityForm" id="entityForm" style="display: flex; gap: 1em;">
        <div>
        <label><h3>Введите название</h3></label>
        <input type="hidden" name="id" />
        <input type="text" name="name" id="name" required style="width: 100%; padding: 8px; box-sizing: border-box;" />
        <div id="nameError" style="color:red; font-size: 0.9em; margin-top: 4px;"></div>
        </div>
    `;

    if (entity === 'category') {
    formHtml += `
        <div>
        <label><h3>Тип</h3></label>
        <select name="type" id="typeSelect" style="width: 100%; padding: 8px;"></select>
        </div>
    `;
    } else if (entity === 'subcategory') {
    formHtml += `
        <div>
        <label><h3>Категория</h3></label>
        <select name="category" id="categorySelect" style="width: 100%; padding: 8px;"></select>
        </div>
    `;
    }

    formHtml += `

        <div>
        <button class="capcodeInput" type="submit" style="margin-top: 50px;">Сохранить</button>
        </div>
    </form>
    `;

  container.innerHTML = formHtml;

  if (entity === 'category') {
    fetchOptions('type', 'typeSelect');
  } else if (entity === 'subcategory') {
    fetchOptions('category', 'categorySelect');
  }

  document.getElementById('entityForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const json = Object.fromEntries(formData.entries());

    const nameErrorDiv = document.getElementById('nameError');
    nameErrorDiv.textContent = '';

    try {
        await apiRequest(`${endpoints[entity]}/save`, 'POST', json);
        renderAdminSection(entity);
        } catch (error) {
        if (typeof error === 'object' && error.name) {
            const message = error.name.join(', ');
            console.log("message", message)
            Swal.fire({
            icon: 'error',
            title: 'Ошибка!',
            text: message,
            confirmButtonText: 'Ок',
            });
        } else {
            console.log("message")

            Swal.fire({
            icon: 'error',
            title: 'Ошибка!',
            text: 'Ошибка при сохранении',
            confirmButtonText: 'Ок',
            });
        }
        }
  });
}

async function fetchOptions(entity, selectId) {
  const select = document.getElementById(selectId);
  if (!select) return;

  const data = await apiRequest(`${endpoints[entity]}/getlist`);
  select.innerHTML = data
    .map(item => `<option value="${item.id}">${item.name}</option>`)
    .join('');
}

function renderList(entity, data, container) {
  if (!Array.isArray(data)) {
    container.innerHTML = '<p>Нет данных</p>';
    return;
  }

  const table = document.createElement('table');
  table.innerHTML = `<tr><th>Название</th><th>Действия</th></tr>`;

  data.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.name}</td>
      <td>
        <button data-id="${item.id}" class="edit-btn btn btn-light btn-sm">
          <i class="bi bi-pencil"></i>
        </button>
        <button data-id="${item.id}" class="delete-btn btn btn-light btn-sm">
          <i class="bi bi-trash"></i>
        </button>
      </td>
    `;
    table.appendChild(row);
  });

  container.appendChild(table);

  container.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async () => {
      await apiRequest(`${endpoints[entity]}/delete`, 'POST', { ids: [parseInt(btn.dataset.id)] });
      await renderAdminSection(entity);
    });
  });

  container.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = data.find(i => i.id == btn.dataset.id);
      const form = document.getElementById('entityForm');
      if (form) {
        Object.keys(item).forEach(k => {
          if (form.elements[k]) {
            form.elements[k].value = item[k];
          }
        });
      }
    });
  });
}

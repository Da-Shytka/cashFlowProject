import { apiRequest } from '../../api.js';

document.addEventListener('DOMContentLoaded', () => {
  loadAllDictionaries().then(() => {
    loadOperations();
    populateFilters();
    setupFilterEvents();
  });
});

let statuses = {};
let types = {};
let categories = {};
let subcategories = {};

async function loadDictionary(path) {
  const list = await apiRequest(path);
  const dict = {};
  list.forEach(item => {
    dict[item.id] = item.name;
  });
  return dict;
}

async function loadAllDictionaries() {
  [statuses, types, categories, subcategories] = await Promise.all([
    loadDictionary('status/getlist'),
    loadDictionary('type/getlist'),
    loadDictionary('category/getlist'),
    loadDictionary('subcategory/getlist'),
  ]);
}

function populateFilters() {
  populateSelect('statusFilter', statuses);
  populateSelect('typeFilter', types);
  populateSelect('categoryFilter', categories);
  populateSelect('subcategoryFilter', subcategories);
}

function populateSelect(selectId, dictionary) {
  const select = document.getElementById(selectId);
  Object.entries(dictionary).forEach(([id, name]) => {
    const option = document.createElement('option');
    option.value = id;
    option.textContent = name;
    select.appendChild(option);
  });
}

function setupFilterEvents() {
  const filtersForm = document.getElementById('filtersForm');
  const resetBtn = document.getElementById('resetFilters');

  filtersForm.addEventListener('submit', (e) => {
    e.preventDefault();
    loadOperations();
  });

  resetBtn.addEventListener('click', () => {
    filtersForm.reset();
    loadOperations();
  });

  document.getElementById('categoryFilter').addEventListener('change', function() {
    const categoryId = this.value;
    const subcategorySelect = document.getElementById('subcategoryFilter');
    subcategorySelect.innerHTML = '<option value="">Все</option>';
    
    if (categoryId) {
      Object.entries(subcategories).forEach(([id, name]) => {
        const option = document.createElement('option');
        option.value = id;
        option.textContent = name;
        subcategorySelect.appendChild(option);
      });
    }
  });
}

async function loadOperations() {
  const loadingEl = document.getElementById('loading');
  const errorEl = document.getElementById('error');
  const tableContainer = document.querySelector('.table-responsive');
  const table = document.getElementById('operationsTable');
  const thead = table.querySelector('thead');
  const tbody = table.querySelector('tbody');

  loadingEl.style.display = 'block';
  errorEl.style.display = 'none';
  tableContainer.style.display = 'none';

  try {
    const filters = {
      start_date: document.getElementById('startDate').value,
      end_date: document.getElementById('endDate').value,
      status: document.getElementById('statusFilter').value,
      type: document.getElementById('typeFilter').value,
      category: document.getElementById('categoryFilter').value,
      subcategory: document.getElementById('subcategoryFilter').value,
    };

    const queryParams = new URLSearchParams();
    for (const [key, value] of Object.entries(filters)) {
      if (value) {
        queryParams.append(key, value);
      }
    }

    const operations = await apiRequest(`operation/getlist?${queryParams.toString()}`);

    if (!operations.length) {
      loadingEl.textContent = 'Нет данных, соответствующих выбранным фильтрам';
      tableContainer.style.display = 'none';
      return;
    }

    loadingEl.style.display = 'none';
    tableContainer.style.display = 'block';

    thead.innerHTML = `
      <tr>
        <th>Статус</th>
        <th>Тип</th>
        <th>Категория</th>
        <th>Подкатегория</th>
        <th>Сумма</th>
        <th>Дата</th>
        <th>Комментарий</th>
        <th>Действия</th>
      </tr>
    `;

    tbody.innerHTML = '';

    operations.forEach(op => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${escapeHtml(statuses[op.status] || op.status)}</td>
        <td>${escapeHtml(types[op.type] || op.type)}</td>
        <td>${escapeHtml(categories[op.category] || op.category)}</td>
        <td>${escapeHtml(subcategories[op.subcategory] || op.subcategory)}</td>
        <td>${Number(op.amount).toFixed(2)}</td>
        <td>${escapeHtml(op.date)}</td>
        <td>${escapeHtml(op.comment || '')}</td>
        <td>
          <button data-id="${op.id}" class="edit-btn btn btn-light btn-sm">
            <i class="bi bi-pencil"></i>
          </button>
          <button data-id="${op.id}" class="delete-btn btn btn-light btn-sm">
            <i class="bi bi-trash"></i>
          </button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    tbody.querySelectorAll('.delete-btn').forEach(btn => {
      btn.addEventListener('click', onDeleteOperation);
    });

    tbody.querySelectorAll('.edit-btn').forEach(btn => {
      btn.addEventListener('click', onEditOperation);
    });

  } catch (error) {
    loadingEl.style.display = 'none';
    errorEl.style.display = 'block';
    errorEl.textContent = 'Ошибка загрузки операций: ' + error.message;
  }
}

async function onDeleteOperation(e) {
  const id = e.currentTarget.dataset.id;  
  console.log('Удаляем операцию с id=', id);
  
  try {
    await apiRequest(`operation/delete`, 'POST', { ids: [parseInt(id)] });
    console.log('Удаление прошло успешно');
    await loadOperations();
  } catch (error) {
    console.error('Ошибка удаления операции:', error);
    alert('Ошибка удаления операции: ' + error.message);
  }
}

function onEditOperation(e) {
  const id = e.currentTarget.dataset.id;
  console.log("id", id)
  apiRequest(`operations/${id}/`,).then(op => {
    sessionStorage.setItem('editOperation', JSON.stringify(op));
    location.href = 'notes.html';
  }).catch(err => {
    alert('Ошибка загрузки операции для редактирования: ' + err.message);
  });
}

function escapeHtml(text) {
  if (!text) return '';
  return text.replace(/[&<>"']/g, function(m) {
    return ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    })[m];
  });
}

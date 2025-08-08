import { apiRequest } from '../../api.js';

document.addEventListener('DOMContentLoaded', async () => {
  await renderOperationForm();

  const editOpData = sessionStorage.getItem('editOperation');
  if (editOpData) {
    console.log("editOpData", editOpData)
    const opsArray = JSON.parse(editOpData);
    const op = Array.isArray(opsArray) ? opsArray[0] : opsArray;

    sessionStorage.removeItem('editOperation');

    fillFormData(op);
  }
});

async function fillFormData(op) {
  const form = document.getElementById('operationForm');
  if (!form.querySelector('input[name="id"]')) {
    const idInput = document.createElement('input');
    idInput.type = 'hidden';
    idInput.name = 'id';
    idInput.value = op.id || '';
    form.appendChild(idInput);
  } else {
    form.querySelector('input[name="id"]').value = op.id || '';
  }

  const statusEl = document.getElementById('status');
  const typeEl = document.getElementById('type');
  const categoryEl = document.getElementById('category');
  const subcategoryEl = document.getElementById('subcategory');
  const amountEl = document.getElementById('amount');
  const dateEl = document.getElementById('date');
  const commentEl = document.getElementById('comment');

  if (!statusEl || !typeEl || !categoryEl || !subcategoryEl || !amountEl || !dateEl || !commentEl) {
    console.warn('Не найдены все поля формы для заполнения');
    return;
  }

  statusEl.value = op.status || '';
  typeEl.value = op.type || '';

  await updateCategoriesByType(op.type, false);

  categoryEl.value = op.category || '';

  await loadSubcategories(op.category, false);

  subcategoryEl.value = op.subcategory || '';

  amountEl.value = op.amount || '';
  dateEl.value = op.date || '';
  commentEl.value = op.comment || '';
}

async function renderOperationForm() {
  const container = document.getElementById('operationFormContainer');
  
  if (!container) {
    console.error('Контейнер для формы не найден');
    document.body.innerHTML += '<div style="color:red">Контейнер #operationFormContainer не найден</div>';
    return;
  }

  const formHtml = `
    <form id="operationForm" class="operation-form">
      <div class="form-row">
        <div class="form-group">
          <label for="status">Статус:</label>
          <select id="status" name="status" required>
            <option value="">Выберите статус</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="type">Тип операции:</label>
          <select id="type" name="type" required>
            <option value="">Выберите тип</option>
          </select>
        </div>
      </div>
      
      <div class="form-group">
        <label for="category">Категория:</label>
        <select id="category" name="category" required>
          <option value="">Выберите категорию</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="subcategory">Подкатегория:</label>
        <select id="subcategory" name="subcategory" required disabled>
          <option value="">Сначала выберите категорию</option>
        </select>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label for="amount">Сумма:</label>
          <input type="number" id="amount" name="amount" step="0.01" required>
        </div>
        
        <div class="form-group">
          <label for="date">Дата:</label>
          <input type="date" id="date" name="date" required>
        </div>
      </div>
      
      <div class="form-group">
        <label for="comment">Комментарий:</label>
        <textarea id="comment" name="comment" rows="3"></textarea>
      </div>
      
      <button type="submit" class="submit-btn">Сохранить</button>
    </form>
  `;
  
  container.innerHTML = formHtml;

  await Promise.all([
    loadTypes(),
    loadStatuses(),
    loadCategories()
  ]);
  
  document.getElementById('type').addEventListener('change', async function() {
    const typeId = this.value;
    await updateCategoriesByType(typeId);
  });
  
  document.getElementById('category').addEventListener('change', async function() {
    const categoryId = this.value;
    await loadSubcategories(categoryId);
  });
  
  document.getElementById('operationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    await saveOperation();
  });
  
  document.getElementById('date').valueAsDate = new Date();
}

async function updateCategoriesByType(typeId) {
  const categorySelect = document.getElementById('category');
  const subcategorySelect = document.getElementById('subcategory');
  
  if (!typeId) {
    categorySelect.innerHTML = '<option value="">Выберите категорию</option>';
    subcategorySelect.innerHTML = '<option value="">Сначала выберите категорию</option>';
    subcategorySelect.disabled = true;
    return;
  }
  
  try {
    const categories = await apiRequest('category/getlist');
    
    const filteredCategories = categories.filter(category => category.type == typeId);
    
    categorySelect.innerHTML = '';
    categorySelect.disabled = false;
    
    if (filteredCategories.length === 0) {
      categorySelect.innerHTML = '<option value="">Нет категорий для выбранного типа</option>';
      subcategorySelect.innerHTML = '<option value="">Нет доступных подкатегорий</option>';
      subcategorySelect.disabled = true;
      return;
    }
    
    filteredCategories.forEach(category => {
      const option = document.createElement('option');
      option.value = category.id;
      option.textContent = category.name;
      categorySelect.appendChild(option);
    });
    
    if (filteredCategories.length > 0) {
      categorySelect.value = filteredCategories[0].id;
      await loadSubcategories(filteredCategories[0].id);
    }
  } catch (error) {
    console.error('Ошибка загрузки категорий по типу:', error);
    alert('Не удалось загрузить категории для выбранного типа');
  }
}

async function loadTypes() {
  try {
    const types = await apiRequest('type/getlist');
    const typeSelect = document.getElementById('type');
    
    types.forEach(type => {
      const option = document.createElement('option');
      option.value = type.id;
      option.textContent = type.name;
      typeSelect.appendChild(option);
    });
  } catch (error) {
    console.error('Ошибка загрузки типов:', error);
    alert('Не удалось загрузить типы операций');
  }
}

async function loadStatuses() {
  try {
    const statuses = await apiRequest('status/getlist');
    const statusSelect = document.getElementById('status');
    
    statuses.forEach(status => {
      const option = document.createElement('option');
      option.value = status.id;
      option.textContent = status.name;
      statusSelect.appendChild(option);
    });
  } catch (error) {
    console.error('Ошибка загрузки статусов:', error);
    alert('Не удалось загрузить статусы');
  }
}

async function loadCategories() {
  try {
    const categories = await apiRequest('category/getlist');
    const categorySelect = document.getElementById('category');
    
    categorySelect.dataset.allCategories = JSON.stringify(categories);
    
    categorySelect.innerHTML = '<option value="">Сначала выберите тип операции</option>';
    categorySelect.disabled = true;
  } catch (error) {
    console.error('Ошибка загрузки категорий:', error);
    alert('Не удалось загрузить категории');
  }
}

async function loadSubcategories(categoryId) {
  const subcategorySelect = document.getElementById('subcategory');
  
  if (!categoryId) {
    subcategorySelect.innerHTML = '<option value="">Сначала выберите категорию</option>';
    subcategorySelect.disabled = true;
    return;
  }
  
  try {
    const subcategories = await apiRequest('subcategory/getlist');
    const filteredSubcategories = subcategories.filter(sub => sub.category == categoryId);
    
    subcategorySelect.innerHTML = '';
    subcategorySelect.disabled = false;
    
    if (filteredSubcategories.length === 0) {
      subcategorySelect.innerHTML = '<option value="">Нет подкатегорий для выбранной категории</option>';
      return;
    }
    
    filteredSubcategories.forEach(subcategory => {
      const option = document.createElement('option');
      option.value = subcategory.id;
      option.textContent = subcategory.name;
      subcategorySelect.appendChild(option);
    });
    
    if (filteredSubcategories.length > 0) {
      subcategorySelect.value = filteredSubcategories[0].id;
    }
  } catch (error) {
    console.error('Ошибка загрузки подкатегорий:', error);
    alert('Не удалось загрузить подкатегории');
  }
}

async function saveOperation() {
  const form = document.getElementById('operationForm');
  const formData = new FormData(form);
  const jsonData = Object.fromEntries(formData.entries());
  
  try {
    await apiRequest('operation/save', 'POST', jsonData);
    alert('Операция успешно сохранена');
    form.reset();
    document.getElementById('date').valueAsDate = new Date();
  } catch (error) {
    console.error('Ошибка сохранения операции:', error);
    alert('Не удалось сохранить операцию');
  }
}
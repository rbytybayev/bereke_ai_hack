<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI-Ассистент по валютному контролю</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    .result-icon {
      font-size: 1.5rem;
    }
    .result-icon.success { color: green; }
    .result-icon.fail { color: red; }
    .law-ref { font-size: 0.9rem; color: #666; }
  </style>
</head>
<body class="bg-light">
<div class="container py-4">
  <div class="row mb-4">
    <div class="col-md-3">
      <img src="logo_bank.png" alt="Bereke Bank" class="img-fluid">
    </div>
    <div class="col-md-9">
      <h4>AI-Ассистент по валютному контролю и комплаенсу</h4>
    </div>
  </div>

  <div class="card mb-3">
    <div class="card-body">
      <form id="uploadForm" enctype="multipart/form-data">
        <div class="mb-3">
          <label for="pdfFile" class="form-label">Загрузите файл для проверки</label>
          <input class="form-control" type="file" id="pdfFile" name="file" required>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="check1" name="check1" checked>
          <label class="form-check-label" for="check1">
            Проверка валютного законодательства
          </label>
        </div>
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="check2" name="check2">
          <label class="form-check-label" for="check2">
            Проверка по санкционным спискам/комплаенсу
          </label>
        </div>
        <button type="submit" class="btn btn-success mt-3">Запустить проверку</button>
      </form>
    </div>
  </div>

  <div class="card" id="resultCard" style="display:none">
    <div class="card-header">
      <strong>Результат анализа</strong>
    </div>
    <div class="card-body">
      <ul class="nav nav-tabs mb-3">
        <li class="nav-item">
          <a class="nav-link active" data-bs-toggle="tab" href="#check-law">Проверка валютного законодательства</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" data-bs-toggle="tab" href="#check-sanctions">Проверка по санкционным спискам/комплаенсу</a>
        </li>
      </ul>
      <div class="tab-content">
        <div class="tab-pane fade show active" id="check-law">
          <table class="table table-bordered">
            <thead class="table-light">
              <tr>
                <th>Критерии</th>
                <th>Результат</th>
                <th>Комментарии</th>
                <th>Ссылка на фрагмент</th>
                <th>Ссылка на закон</th>
              </tr>
            </thead>
            <tbody id="lawResults">
              <!-- JS will populate rows here -->
            </tbody>
          </table>
        </div>
        <div class="tab-pane fade" id="check-sanctions">
          <p class="text-muted">Функционал в разработке...</p>
        </div>
      </div>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
  document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const res = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    renderResults(data);
  });

  function renderResults(data) {
    document.getElementById('resultCard').style.display = 'block';
    const table = document.getElementById('lawResults');
    table.innerHTML = '';
    data.results.forEach(item => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${item.label}</td>
        <td><span class="result-icon ${item.success ? 'success' : 'fail'}">${item.success ? '✔️' : '❌'}</span></td>
        <td>${item.comment || ''}</td>
        <td>${item.fragment_url ? '<a href="' + item.fragment_url + '">🔗</a>' : ''}</td>
        <td>${item.law_reference || ''}</td>
      `;
      table.appendChild(row);
    });
  }
</script>
</body>
</html>

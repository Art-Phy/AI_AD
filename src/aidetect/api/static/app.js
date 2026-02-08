
const btn = document.getElementById('btn');
const out = document.getElementById('output');

btn.addEventListener('click', async () => {
  const text = document.getElementById('text').value;
  const mode = document.getElementById('mode').value;
  const apiKey = document.getElementById('apiKey').value;

  out.hidden = false;
  out.textContent = 'Analizando...';
  btn.classList.add('loading');

  try {
    const url = `/v1/analyze/text?api_key=${encodeURIComponent(apiKey)}`;

    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
      body: JSON.stringify({ text, mode })
    });

    const data = await res.json();
    if (!res.ok) {
      out.textContent = `Error ${res.status}:\n` + JSON.stringify(data, null, 2);
    } else {
      out.textContent = JSON.stringify(data, null, 2);
    }
  } catch (err) {
    out.textContent = 'Error de conexión: ' + err;
  } finally {
    btn.classList.remove('loading');
  }
});

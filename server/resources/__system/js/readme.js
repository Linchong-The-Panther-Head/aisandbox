// README表示ページの初期化処理 / initialize README view
document.addEventListener('DOMContentLoaded', () => {
  setLang(currentLang);
  loadReadme();
  const ja = document.getElementById('lang-ja');
  const en = document.getElementById('lang-en');
  if (ja) ja.addEventListener('click', loadReadme);
  if (en) en.addEventListener('click', loadReadme);
});

// READMEファイルを取得して表示 / fetch and display README
function loadReadme() {
  const file = currentLang === 'ja' ? '/README.ja.md' : '/README.md';
  fetch(file)
    .then(r => r.text())
    .then(t => {
      document.getElementById('readme').textContent = t;
    });
}

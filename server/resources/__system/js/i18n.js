/**
 * 日本語と英語に対応した簡易 i18n ヘルパー。
 * 翻訳したい要素には `data-i18n` 属性を付け、下記 `strings` テーブルのキーを指定します。
 * `setLang('ja')` または `setLang('en')` を呼び出すことで言語を切り替えます。
 * `lang-ja` と `lang-en` の ID を持つボタンが存在すれば自動でハンドラーが登録されます。
 * Basic i18n helper supporting Japanese and English. Elements with a `data-i18n`
 * attribute use keys from the `strings` table. Language toggle buttons with
 * IDs `lang-ja` and `lang-en` call this function on click.
 *
 * @module i18n
 */

/** @type {Object.<string, Object.<string, string>>} */
const strings = {
  ja: {
    welcome: 'ようこそ Simple HTTPS Server へ!',
    editConfig: '設定編集',
    configTitle: 'サーバー設定',
    saveRestart: '保存して再起動',
    host: 'ホスト',
    port: 'ポート',
    domain: 'ドメイン',
    certfile: '証明書ファイル',
    keyfile: '鍵ファイル',
    resourcePath: 'リソースパス',
    requiredError: '必須項目です',
    portError: '1～65535の数字を入力してください',
    portInUse: '指定されたポートは使用中です',
    fileNotFound: 'ファイルが見つかりません',
    dirNotFound: 'ディレクトリが見つかりません',
    hostHelp: '例: 0.0.0.0 や 127.0.0.1',
    portHelp: '1～65535 のポート番号 (例: 8443)',
    domainHelp: '参照用ドメイン名 (例: example.com)',
    certfileHelp: '証明書ファイルへのパス (例: server/cert.pem)',
    keyfileHelp: '鍵ファイルへのパス (例: server/key.pem)',
    resourcePathHelp: '静的リソースのディレクトリ (例: server/resources)',
    viewReadme: 'README を表示',
    openSample: 'サンプルを開く',
    readmeTitle: 'README'
  },
  en: {
    welcome: 'Welcome to the Simple HTTPS Server!',
    editConfig: 'Edit Configuration',
    configTitle: 'Server Configuration',
    saveRestart: 'Save & Restart',
    host: 'Host',
    port: 'Port',
    domain: 'Domain',
    certfile: 'Certificate File',
    keyfile: 'Key File',
    resourcePath: 'Resource Path',
    requiredError: 'Required field',
    portError: 'Enter a number between 1 and 65535',
    portInUse: 'Specified port is already in use',
    fileNotFound: 'File not found',
    dirNotFound: 'Directory not found',
    hostHelp: 'Address to bind the server (e.g., 0.0.0.0)',
    portHelp: 'Port number 1-65535 (e.g., 8443)',
    domainHelp: 'Domain name for reference (e.g., example.com)',
    certfileHelp: 'Path to TLS certificate (e.g., server/cert.pem)',
    keyfileHelp: 'Path to private key (e.g., server/key.pem)',
    resourcePathHelp: 'Directory of static files (e.g., server/resources)',
    viewReadme: 'View README',
    openSample: 'Open Sample',
    readmeTitle: 'README'
  }
};

/** @type {string} */
let currentLang = 'ja';

const urlLang = new URLSearchParams(location.search).get('lang');
const storedLang = localStorage.getItem('lang');
if (urlLang && strings[urlLang]) {
  currentLang = urlLang;
} else if (storedLang && strings[storedLang]) {
  currentLang = storedLang;
}

/**
 * すべての翻訳対象要素を指定した言語に更新します。
 * Update all translatable elements to the specified language.
 * @param {string} lang - 'ja' or 'en'
 */
function setLang(lang) {
  if (!strings[lang]) return;
  currentLang = lang;
  localStorage.setItem('lang', lang);
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const str = strings[lang][key];
    if (!str) return;
    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
      el.placeholder = str;
    } else {
      el.textContent = str;
    }
  });
  document.querySelectorAll('[data-help-key]').forEach(el => {
    const key = el.getAttribute('data-help-key');
    el.setAttribute('data-help', strings[lang][key] || '');
  });
}

/**
 * 現在の言語で翻訳された文字列を取得します。
 * Retrieve a translated string for the current language.
 * @param {string} key - translation key
 * @returns {string}
 */
function t(key) {
  return strings[currentLang][key] || key;
}

document.addEventListener('DOMContentLoaded', () => {
  setLang(currentLang);
  const btnJa = document.getElementById('lang-ja');
  const btnEn = document.getElementById('lang-en');
  if (btnJa) btnJa.addEventListener('click', () => setLang('ja'));
  if (btnEn) btnEn.addEventListener('click', () => setLang('en'));
});

/**
 * Configuration editor logic.
 * Validates form fields and posts updates to the server.
 * Error messages are localized via the global `t()` function.
 *
 * @module config
 */

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('config-form');
  const submitBtn = document.getElementById('submit-btn');
  if (!form || !submitBtn) return;

  /** @type {string[]} */
  const fields = ['host', 'port', 'domain', 'certfile', 'keyfile', 'resource_path'];
  /** @type {Object.<string, string>} */
  const errors = {};

  /**
   * Convert full-width digits to half-width.
   * @param {string} s
   * @returns {string}
   */
  const toHalfWidth = s => s.replace(/[０-９]/g, ch => String.fromCharCode(ch.charCodeAt(0) - 0xFEE0));

  /**
   * Validate a single field and display an error message if necessary.
   * @param {string} name
   */
  function validateField(name) {
    const el = form.elements[name];
    let v = toHalfWidth(el.value.trim());
    el.value = v;
    let err = '';
    if (name === 'port') {
      if (!/^[0-9]+$/.test(v) || Number(v) < 1 || Number(v) > 65535) {
        err = t('portError');
      }
    } else {
      if (v === '') {
        err = t('requiredError');
      }
    }
    document.getElementById('error-' + name).textContent = err;
    errors[name] = err;
    updateSubmit();
  }

  /** Enable or disable the submit button based on current errors. */
  function updateSubmit() {
    const hasError = fields.some(f => errors[f]);
    submitBtn.disabled = hasError;
  }

  fields.forEach(name => {
    const el = form.elements[name];
    el.addEventListener('blur', () => validateField(name));
  });

  // Load initial configuration
  fetch('/config').then(r => r.json()).then(cfg => {
    Object.keys(cfg).forEach(key => {
      if (form.elements[key]) {
        form.elements[key].value = cfg[key];
      }
    });
    fields.forEach(f => validateField(f));
  });

  form.addEventListener('submit', e => {
    e.preventDefault();
    fields.forEach(f => validateField(f));
    const hasError = fields.some(f => errors[f]);
    if (hasError) return;
    /** @type {Object.<string, string|boolean>} */
    const data = {};
    fields.forEach(name => {
      data[name] = form.elements[name].value;
    });
    data.restart = true;
    fetch('/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(r => r.text())
      .then(txt => {
        document.getElementById('status').textContent = txt;
      })
      .catch(() => {
        document.getElementById('status').textContent = 'Error';
      });
  });
});

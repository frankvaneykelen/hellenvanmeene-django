/**
 * Auto-generate the Foldername slug from the Title field in Django admin.
 *
 * Rules:
 *  - Only auto-fills while the foldername is still empty (or was empty on page-load).
 *  - Once the user manually edits foldername the auto-fill stops.
 *  - Slugifies: lowercases, strips diacritics, replaces anything non-alphanumeric
 *    with a hyphen, collapses runs of hyphens, trims leading/trailing hyphens.
 */
(function () {
  'use strict';

  function slugify(text) {
    return text
      .toLowerCase()
      // decompose accented characters then strip combining marks
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      // replace anything that's not a-z, 0-9 with a hyphen
      .replace(/[^a-z0-9]+/g, '-')
      // collapse multiple hyphens
      .replace(/-{2,}/g, '-')
      // trim leading/trailing hyphens
      .replace(/^-+|-+$/g, '');
  }

  function init() {
    var titleField    = document.getElementById('id_title');
    var folderField   = document.getElementById('id_foldername');

    if (!titleField || !folderField) return;

    // If foldername already has a value on page-load, don't touch it.
    var autoFill = folderField.value.trim() === '';

    // User manually edits foldername → stop auto-fill.
    folderField.addEventListener('input', function () {
      autoFill = false;
    });

    titleField.addEventListener('input', function () {
      if (!autoFill) return;
      folderField.value = slugify(titleField.value);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

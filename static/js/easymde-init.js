/* Initialize EasyMDE on any textarea with class 'easymde-widget'. */
(function () {
  function init() {
    document.querySelectorAll('textarea.easymde-widget').forEach(function (el) {
      if (el._easymde) return; // already initialised
      el._easymde = new EasyMDE({
        element: el,
        spellChecker: false,
        autosave: { enabled: false },
        toolbar: [
          'bold', 'italic', 'heading', '|',
          'quote', 'unordered-list', 'ordered-list', '|',
          'link', 'code', '|',
          'preview', 'side-by-side', 'fullscreen', '|',
          'guide',
        ],
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  /* Re-run after Django admin inline rows are added. */
  document.addEventListener('formset:added', init);
})();

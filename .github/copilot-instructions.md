# Copilot Instructions — hellenvanmeene-django

## General

- Address the developer as **Frank**, not "the user".

---

## Styling — Bootstrap 5 + Color Admin

- This project uses **Color Admin v5.5.2** on top of Bootstrap 5.
- The compiled theme assets live in `static/css/e-commerce/app.min.css`.
- The original template source is at `C:\web-templates-and-design-assets\color_admin_v5.5.2`.
- The theme's homepage is at https://wrapmarket.com/item/color-admin-admin-template-frontend-WB0N89JMK.
- The preview is at https://wrapmarket.com/item/WB0N89JMK/preview.
- The theme has two parts:
  - Admin: [documentation](../web-templates-and-design-assets/color_admin_v5.5.2/admin/documentation/index.html)
  - Frontend: [documentation](../web-templates-and-design-assets/color_admin_v5.5.2/frontend/documentation/index.html)
- The frontend part is what we use for the public-facing site. It includes a large set of pre-designed UI components (badges, buttons, alerts, cards, timelines, etc.) that we can use as building blocks for our pages. It also has a rich colour palette with multiple tonal variations for each colour (e.g. `bg-warning-100`, `bg-warning-200`, ..., `bg-warning-900`).

### When suggesting HTML/CSS for a UI component:

1. **Start with vanilla Bootstrap 5** — prefer the standard BS5 class names (e.g. `badge text-bg-warning`, `btn btn-primary`, `alert alert-info`).  
   The theme inherits all BS5 utilities, so they always work.

2. **Check Color Admin for an enhanced alternative** — look in  
   `C:\web-templates-and-design-assets\color_admin_v5.5.2\template\` for relevant page or component examples (e.g. `ui_badge.html`, `ui_buttons.html`, `page_timeline.html`).  
   Color Admin often provides richer variants (extra colours, size modifiers, icon-integrated components, theme-specific patterns).

3. **Present Frank with a choice** — show both options with a brief note on the difference, e.g.:

   > **Option A — Bootstrap 5 (standard)**
   > ```html
   > <span class="badge text-bg-warning">new</span>
   > ```
   >
   > **Option B — Color Admin** (if a richer variant exists)
   > ```html
   > <span class="badge bg-warning-200 text-warning-800">new</span>
   > ```
   > Color Admin adds a full tonal palette (`-100` → `-900`) for each colour.

4. Only the single `.github/copilot-instructions.md` file governs custom instructions — do not create additional `.md` summary or documentation files unless Frank explicitly asks.

---

## Shell / CLI

- Frank is on **Windows / PowerShell**. Always write shell commands as PowerShell.
- Use backtick (`` ` ``) for line continuation — never `\`.
- Use `powershell` as the code-fence language tag for terminal commands, not `bash` or `sh`.

---

## Django / Python

- `MIGRATION_MODULES` for legacy apps is set to `None` — use `migrate --run-syncdb` for those apps, and `makemigrations` + `migrate` for apps that do have migrations (e.g. `galleries`, `links`, `shop`).
- `DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"` — all PKs/FKs are `bigint`.
- SCSS source: `static/scss/hellenvanmeene-website-custom.scss` — compiled automatically by `CoreConfig.ready()` on Django start. Never edit the compiled `static/css/hellenvanmeene-website-custom.css` by hand.
- Settings are split: `config/settings/base.py`, `dev.py`, `prod.py`; run with `DJANGO_SETTINGS_MODULE=config.settings.dev`.

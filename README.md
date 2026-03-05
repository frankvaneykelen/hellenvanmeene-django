# hellenvanmeene-django

Django 5.2 rewrite of [hellenvanmeene.com](https://hellenvanmeene.com) — a photographer's portfolio and archive site.

## TL;DR;

```
PS C:\git\hellenvanmeene-django> python -m venv .venv

PS C:\git\hellenvanmeene-django> .venv\Scripts\activate

(.venv) PS C:\git\hellenvanmeene-django> python manage.py runserver

http://localhost:8000/admin/
```

## Tech stack

| Layer | Choice |
|---|---|
| Framework | Django 5.2 / Python 3.12 |
| Database | Azure SQL Server (mssql-django 1.6) |
| Storage | Azure Blob Storage (django-storages) |
| Email | SendGrid (django-anymail) |
| Static files | Whitenoise (dev) / Azure Blob (prod) |
| Images | django-imagekit + Pillow |
| Config | python-decouple |
| WSGI server | Gunicorn |
| Infra | Bicep (Azure Linux App Service) |
| CI/CD | GitHub Actions + OIDC |

---

## Local development

### 1. Prerequisites

- Python 3.12
- ODBC Driver 18 for SQL Server ([install](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server))
- Access to the Azure SQL database (or a local SQL Server instance)

### 2. Clone and create virtualenv

```powershell
git clone https://github.com/frankvaneykelen/hellenvanmeene-django.git
cd hellenvanmeene-django
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements/dev.txt
```

### 3. Configure environment

```powershell
Copy-Item .env.example .env
# Edit .env with your database credentials and storage keys
```

### 4. Run migrations

```powershell
python manage.py migrate
```

> **Note**: The existing Azure SQL database already contains the legacy tables. 
> Django will create its own tables alongside them. Run `inspectdb` first to verify 
> the db_table names match before running migrations:
> ```
> python manage.py inspectdb
> ```

### 5. Create a superuser

```powershell
python manage.py createsuperuser
```

### 6. Start the dev server

```powershell
python manage.py runserver
```

Admin panel: http://localhost:8000/admin/

---

## Project structure

```
config/               # Django project package
  settings/
    base.py           # shared settings (DB, storage, email, apps)
    dev.py            # local overrides (DEBUG=True, console email)
    prod.py           # production (HTTPS, HSTS, Azure logging)
  urls.py
  wsgi.py / asgi.py

core/                 # Shared reference models (Country, Place, Location, Creator, Tag, …)
photos/               # Photo model — core asset of the site
exhibitions/          # Exhibition + through-tables (creators, media, publications, tags)
events/               # Event + EventTag
news/                 # NewsArticle + images + tags
pages/                # Page (self-referential tree) + PageTag
publications/         # Publication + creators + tags
shop/                 # Product (placeholder)

requirements/
  base.txt            # production packages
  dev.txt             # + django-debug-toolbar
  prod.txt            # = base.txt (Gunicorn included in base)

infra/                # Bicep — Azure Linux App Service
.github/workflows/    # GitHub Actions CI/CD
```

---

## Frontend template — Color Admin v5.5.2

The public-facing site uses the **Color Admin v5.5.2** commercial Bootstrap theme.
The compiled CSS, JS, and webfonts are committed to this repo under `static/` so the
site works without any extra build step. The raw template source (Sass, unminified JS,
PSD files, etc.) is **not** committed — it is `.gitignore`d — because it is a
paid asset.

**Purchase / download link:**
https://wrapmarket.com/item/color-admin-admin-template-frontend-WB0N89JMK

### Setting up the template on a fresh clone

If you have just cloned this repo on a new laptop and the pre-built assets are already
present in `static/css/e-commerce/`, `static/js/e-commerce/`, and `static/css/webfonts/`
you do **not** need to do anything — skip this section.

If for any reason the `static/` assets are missing (e.g. you are starting from the
source zip), follow these steps:

1. **Purchase** the template at the link above and download the zip.
2. **Extract** the zip. You will find a folder called `frontend/` inside the archive.
3. **Copy the pre-built assets** into this repo:

```powershell
# Replace <COLOR_ADMIN_ROOT> with the path where you extracted the zip.
$src = "<COLOR_ADMIN_ROOT>\frontend\template\e-commerce"
$repo = "C:\git\hellenvanmeene-django"

# CSS
Copy-Item "$src\assets\css\vendor.min.css"  "$repo\static\css\e-commerce\vendor.min.css" -Force
Copy-Item "$src\assets\css\app.min.css"     "$repo\static\css\e-commerce\app.min.css"    -Force

# Webfonts referenced by vendor.min.css via "../webfonts/"
Copy-Item "$src\assets\css\webfonts\*"      "$repo\static\css\webfonts\" -Force

# JS
Copy-Item "$src\assets\js\vendor.min.js"   "$repo\static\js\e-commerce\vendor.min.js"  -Force
Copy-Item "$src\assets\js\app.min.js"      "$repo\static\js\e-commerce\app.min.js"     -Force
```

4. Run `python manage.py collectstatic` as usual for deployment.

> The raw source lives at `web-templates-and-design-assets/color_admin_v5.5.2/`
> (relative to the repo root) if you place the extracted zip there. That path is
> in `.gitignore` and will never be committed.

### Custom CSS overrides

Site-specific CSS overrides are written in SCSS and kept alongside the template:

| File | Purpose |
|---|---|
| `static/scss/hellenvanmeene-website-custom.scss` | **Source** — edit this file |
| `static/css/hellenvanmeene-website-custom.css` | **Compiled output** — do not edit by hand |

`CoreConfig.ready()` (in `core/apps.py`) compiles the SCSS to CSS automatically every
time Django starts, using the `libsass` package. The compiled file is committed to the
repo so that production deployments work without an explicit build step.

**Workflow:**
1. Edit `static/scss/hellenvanmeene-website-custom.scss`
2. Save — the dev server detects the change, restarts, and recompiles the CSS
3. Refresh the browser to see the change
4. Commit **both** the `.scss` source and the compiled `.css`

> **How it works:** `CoreConfig.ready()` hooks into Django's autoreloader via the
> `autoreload_started` signal to register the SCSS file as a watched file. When
> the file changes the server restarts and `_compile_scss()` runs again.

---

## Deployment

### One-time Azure setup

1. Create the OIDC federated credential for this GitHub repo:
   ```powershell
   az ad app federated-credential create `
     --id 51925ea6-776e-4339-b2d6-9d8bec4436ac `
     --parameters '{\"name\":\"hellenvanmeene-django-main\",\"issuer\":\"https://token.actions.githubusercontent.com\",\"subject\":\"repo:frankvaneykelen/hellenvanmeene-django:ref:refs/heads/master\",\"audiences\":[\"api://AzureADTokenExchange\"]}'
   ```

2. Set GitHub secrets on the new repo:
   - `AZURE_CLIENT_ID` = `51925ea6-776e-4339-b2d6-9d8bec4436ac`
   - `AZURE_TENANT_ID` = `7daaa223-9279-4a97-b3f4-253eae4093ab`
   - `AZURE_SUBSCRIPTION_ID` = `3c0a1e74-fe18-4403-ad5d-e6550f162731`

### Bicep

The `infra/bicep/` folder contains the Bicep deployment.

**Structure:**

| File | Purpose |
|---|---|
| `main.bicep` | App Service Plan + Web App, custom hostnames |
| `keyvault.bicep` | KV access policy + secrets (deployed to a separate subscription) |
| `main.bicepparam` | Non-sensitive parameter defaults — reference/documentation only |
| `secrets.bicepparam` | All deployment values — **never commit**, gitignored |
| `secrets.bicepparam.example` | Template — copy to `secrets.bicepparam` and fill in |

> **Note:** `az` only accepts one `.bicepparam` file. Non-sensitive defaults (`location`, `appName`, etc.) are baked into `main.bicep` itself, so `secrets.bicepparam` is the only file needed at deploy time.

> **Cross-subscription:** The Key Vault lives in subscription `3c0a1e74` / RG `frankvaneykelen-blog`. The app deploys into the `hellenvanmeene` RG. `keyvault.bicep` is called as a module with an explicit `scope:` so this is handled automatically.

**First-time setup:**

```powershell
cd infra/bicep
Copy-Item secrets.bicepparam.example secrets.bicepparam
# fill in secrets.bicepparam
```

**Deploy:**

```powershell
az deployment group create `
  --resource-group hellenvanmeene `
  --parameters secrets.bicepparam
```

**What-if (dry run):**

```powershell
az deployment group what-if `
  --resource-group hellenvanmeene `
  --parameters secrets.bicepparam
```

### GitHub Actions

Push to `main` → the workflow:
1. Installs Python deps
2. Runs `collectstatic`
3. Zips the app (excluding .venv, .git, infra)
4. Authenticates to Azure via OIDC
5. Deploys to `hellenvanmeene-django.azurewebsites.net`

---

## Database migration strategy

The Django app targets the **same Azure SQL database** as the existing .NET app.
`db_table` in each model's `Meta` class maps to the original table names.

To avoid running both apps writing to the same tables simultaneously:
1. Deploy Django app first with `DEBUG=False` and the same DB
2. Verify all data is readable via Django admin
3. Switch DNS from the old App Service to the new one
4. Decommission the old .NET app

---

## Running tests

```powershell
python manage.py test
```

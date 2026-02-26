# hellenvanmeene-django

Django 5.2 rewrite of [hellenvanmeene.com](https://hellenvanmeene.com) — a photographer's portfolio and archive site.

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
| Infra | Terraform (Azure Linux App Service) |
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

infra/                # Terraform — Azure Linux App Service
.github/workflows/    # GitHub Actions CI/CD
```

---

## Deployment

### One-time Azure setup

1. Create a Linux App Service Plan (Python on Azure requires Linux):
   ```bash
   az appservice plan create \
     --name frankvaneykelen-linux \
     --resource-group frankvaneykelen-blog \
     --is-linux \
     --sku B1
   ```

2. Create the OIDC federated credential for this new GitHub repo:
   ```bash
   az ad app federated-credential create \
     --id 51925ea6-776e-4339-b2d6-9d8bec4436ac \
     --parameters '{
       "name": "hellenvanmeene-django-main",
       "issuer": "https://token.actions.githubusercontent.com",
       "subject": "repo:frankvaneykelen/hellenvanmeene-django:ref:refs/heads/main",
       "audiences": ["api://AzureADTokenExchange"]
     }'
   ```

3. Set GitHub secrets on the new repo:
   - `AZURE_CLIENT_ID` = `51925ea6-776e-4339-b2d6-9d8bec4436ac`
   - `AZURE_TENANT_ID` = `7daaa223-9279-4a97-b3f4-253eae4093ab`
   - `AZURE_SUBSCRIPTION_ID` = `3c0a1e74-fe18-4403-ad5d-e6550f162731`

### Terraform

```bash
cd infra
cp secrets.tfvars.example secrets.tfvars
# fill in secrets.tfvars

terraform init
terraform plan -var-file=secrets.tfvars
terraform apply -var-file=secrets.tfvars
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

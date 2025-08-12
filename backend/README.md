# LISMS Backend

This directory contains a Django‑based REST API for the Laboratory Inventory and
Sample Management System (LISMS) application.  The models and sample data mirror
the Microsoft SQL Server schema and stored procedures supplied in the
`LISMS Microsoft SQL Server Database.sql` file.  The API exposes each
entity as a RESTful endpoint and provides several aggregated views for
building dashboards on the front end.

## Prerequisites

To run the back end locally you will need:

* Python 3.9 or newer (tested with Python 3.11)
* A working installation of SQL Server or an alternative database.  For
  development you can switch to SQLite by editing the `DATABASES` section
  in `lims_project/settings.py`.
* [pip](https://pip.pypa.io/) to install Python dependencies.
* An ODBC driver for SQL Server (e.g. **ODBC Driver 17 for SQL Server**) if
  connecting to SQL Server.  See the [Microsoft documentation](https://learn.microsoft.com/sql/connect/odbc/)
  for platform‑specific installation instructions.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your database settings in `lims_project/settings.py`.  By
   default the project is configured to connect to SQL Server using the
   `mssql` backend provided by the `mssql-django` package.  If you prefer
   SQLite for local development, comment out the SQL Server section and
   uncomment the SQLite configuration.

4. Apply migrations and create a superuser:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. (Optional) Load initial data.  You can translate the provided SQL
   script into JSON fixtures using SQL Server tools or external scripts
   and import them via `python manage.py loaddata`.

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

The API will be available at [http://localhost:8000/api/](http://localhost:8000/api/).  The Django admin is
accessible at [http://localhost:8000/admin/](http://localhost:8000/admin/).

## Authentication

Authentication is handled via Auth0 JSON Web Tokens (JWTs).  All API
endpoints require authentication by default.  To connect your own Auth0
tenant:

1. Create a new Auth0 application (Regular Web Application) in the
   Auth0 dashboard.
2. Configure an API in Auth0 and note the **Identifier** (this becomes
   the audience in your JWTs).
3. Update the following environment variables when running the server or
   set them in `lims_project/settings.py`:

   ```bash
   export AUTH0_DOMAIN="your-tenant.us.auth0.com"
   export AUTH0_API_AUDIENCE="https://your-api-identifier"
   export DJANGO_SECRET_KEY="super-secret-string"
   ```

4. On the front end, configure the matching Auth0 domain and client ID
   in `frontend/src/config.js`.

The custom authentication backend defined in
`lims_app/authentication.py` verifies incoming JWTs, but does not
automatically create corresponding `UserAccount` instances.  You can
extend the `authenticate` method to map Auth0 users to your Django
models as needed.

## API Overview

Every model is exposed as a set of REST endpoints under `/api/`.  For
example:

* `/api/samples/` – list and create samples
* `/api/samples/<id>/` – retrieve, update or delete a specific sample
* `/api/equipment/` – list and create equipment records
* `/api/dashboard/warehouse-clients/` – returns a list of warehouses with
  the number of distinct clients served
* `/api/dashboard/version-changes/` – returns the average number of days
  between effective date changes for each SOP

Use a tool like [Postman](https://www.postman.com/) or `curl` to
explore the API.  When making authenticated requests include an
`Authorization` header with a bearer token obtained from Auth0.

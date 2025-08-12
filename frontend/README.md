# LISMS Front End

This directory contains the React user interface for the Laboratory
Information and Sample Management System (LISMS).  The UI authenticates users via
Auth0 and consumes the REST API exposed by the Django back end.

## Prerequisites

* Node.js 14 or newer (tested with Node 16 and 18)
* npm 6 or newer
* An Auth0 application configured for Single Page Applications (SPA)

## Setup

1. Install dependencies:

   ```bash
   npm install
   ```

2. Configure your environment variables.  You can either export them in
   your shell or create a `.env` file in this directory.  The following
   variables are supported:

   ```bash
   REACT_APP_API_BASE_URL=http://localhost:8000/api
   REACT_APP_AUTH0_DOMAIN=your-tenant.us.auth0.com
   REACT_APP_AUTH0_CLIENT_ID=your_client_id
   REACT_APP_AUTH0_AUDIENCE=https://your-api-identifier
   ```

   These values must match the configuration in your Auth0 dashboard and
   the Django back end.

3. Start the development server:

   ```bash
   npm start
   ```

   The app will be served at [http://localhost:3000](http://localhost:3000).

## Project Structure

* `src/` – React source files
  * `index.js` – entry point, wraps the app in the Auth0 provider
  * `App.js` – top‑level router and page definitions
  * `config.js` – centralises API and Auth0 settings
  * `components/` – reusable UI components (e.g. the navigation bar)
  * `pages/` – individual pages corresponding to routes
    * `Dashboard.js` – displays charts and a hero banner
    * `SamplesPage.js` – renders a table of samples
    * `EquipmentPage.js` – shows equipment and maintenance logs
    * `HistoryPage.js` – lists SOP version change history
* `public/hero.png` – decorative hero image used on the dashboard

## Authentication

The UI uses the `@auth0/auth0-react` SDK for authentication.  When the
user clicks the **Log In** button they are redirected to Auth0 to
authenticate.  After a successful login the app obtains an access
token which is stored in memory.  API requests automatically attach
this token in an `Authorization` header.

Make sure to configure the **Allowed Callback URLs** and **Allowed
Logout URLs** in your Auth0 application settings to include
`http://localhost:3000` and the domains where you intend to deploy the
application.
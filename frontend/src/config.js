// Configuration for API endpoints and Auth0 settings.

const config = {
  /**
   * Base URL of the back‑end API.  During development the Django server
   * typically runs on http://localhost:8000.  When deploying to
   * production update this value to point at your hosted API.
   */
  apiBaseUrl: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api',

  /**
   * Auth0 parameters.  Replace the placeholder strings with the domain
   * and client ID from your Auth0 dashboard.  The audience should match
   * the API identifier configured for your back end.
   */
  auth0: {
    domain: process.env.REACT_APP_AUTH0_DOMAIN || 'YOUR_AUTH0_DOMAIN',
    clientId: process.env.REACT_APP_AUTH0_CLIENT_ID || 'YOUR_AUTH0_CLIENT_ID',
    audience: process.env.REACT_APP_AUTH0_AUDIENCE || 'YOUR_AUTH0_API_AUDIENCE'
  }
};

export default config;
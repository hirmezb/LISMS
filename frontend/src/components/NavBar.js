import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { Link as RouterLink } from 'react-router-dom';
import Box from '@mui/material/Box';
import { useAuth0 } from '@auth0/auth0-react';

/**
 * The top navigation bar for the LISMS UI.
 *
 * Displays links to the main sections of the application and buttons
 * for logging in and out via Auth0.  When authenticated the user's
 * name is shown on the log out button.
 */
function NavBar() {
  const { isAuthenticated, loginWithRedirect, logout, user } = useAuth0();

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          LISMS Dashboard
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button component={RouterLink} to="/" color="inherit">
            Dashboard
          </Button>
          <Button component={RouterLink} to="/samples" color="inherit">
            Samples
          </Button>
          <Button component={RouterLink} to="/equipment" color="inherit">
            Equipment
          </Button>
          <Button component={RouterLink} to="/history" color="inherit">
            SOP History
          </Button>
        </Box>
        {isAuthenticated ? (
          <Button color="inherit" onClick={() => logout({ returnTo: window.location.origin })}>
            Log Out {user && user.nickname ? `(${user.nickname})` : ''}
          </Button>
        ) : (
          <Button color="inherit" onClick={() => loginWithRedirect()}>Log In</Button>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;
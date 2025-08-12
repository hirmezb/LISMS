import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import config from '../config';

/**
 * Displays a history of SOP version changes.
 */
function HistoryPage() {
  const { getAccessTokenSilently } = useAuth0();
  const [changes, setChanges] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadChanges() {
      try {
        const token = await getAccessTokenSilently();
        const resp = await axios.get(`${config.apiBaseUrl}/version-changes/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setChanges(resp.data);
      } catch (err) {
        console.error(err);
        setError(err);
      }
    }
    loadChanges();
  }, [getAccessTokenSilently]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        SOP Version History
      </Typography>
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error loading history: {error.message}
        </Typography>
      )}
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>SOP</TableCell>
              <TableCell>Old Version</TableCell>
              <TableCell>New Version</TableCell>
              <TableCell>Old Effective Date</TableCell>
              <TableCell>New Effective Date</TableCell>
              <TableCell>Change Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {changes.map((change) => (
              <TableRow key={change.id} hover>
                <TableCell>{change.id}</TableCell>
                <TableCell>{change.sop?.sop_name}</TableCell>
                <TableCell>{change.old_version_number}</TableCell>
                <TableCell>{change.new_version_number}</TableCell>
                <TableCell>{change.old_effective_date}</TableCell>
                <TableCell>{change.new_effective_date}</TableCell>
                <TableCell>{change.change_date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default HistoryPage;
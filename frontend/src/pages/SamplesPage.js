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
 * Displays a table of all samples in the system.
 */
function SamplesPage() {
  const { getAccessTokenSilently } = useAuth0();
  const [samples, setSamples] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadSamples() {
      try {
        const token = await getAccessTokenSilently();
        const resp = await axios.get(`${config.apiBaseUrl}/samples/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setSamples(resp.data);
      } catch (err) {
        console.error(err);
        setError(err);
      }
    }
    loadSamples();
  }, [getAccessTokenSilently]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Samples
      </Typography>
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error loading samples: {error.message}
        </Typography>
      )}
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Product Name</TableCell>
              <TableCell>Stage</TableCell>
              <TableCell>Quantity</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Storage</TableCell>
              <TableCell>Warehouse</TableCell>
              <TableCell>Location</TableCell>
              <TableCell>Received</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {samples.map((sample) => (
              <TableRow key={sample.id} hover>
                <TableCell>{sample.id}</TableCell>
                <TableCell>{sample.product_name}</TableCell>
                <TableCell>{sample.product_stage}</TableCell>
                <TableCell>{sample.quantity}</TableCell>
                <TableCell>{sample.sample_type}</TableCell>
                <TableCell>{sample.storage_conditions}</TableCell>
                <TableCell>{sample.warehouse?.warehouse_facility}</TableCell>
                <TableCell>
                  {sample.location?.location_type} {sample.location?.room_number}
                </TableCell>
                <TableCell>{new Date(sample.time_received).toLocaleString()}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

export default SamplesPage;
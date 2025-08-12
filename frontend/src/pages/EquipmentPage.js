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
import Grid from '@mui/material/Grid';
import config from '../config';

/**
 * Displays equipment and maintenance logs.
 */
function EquipmentPage() {
  const { getAccessTokenSilently } = useAuth0();
  const [equipment, setEquipment] = useState([]);
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const token = await getAccessTokenSilently();
        const headers = { Authorization: `Bearer ${token}` };
        const [equipResp, logsResp] = await Promise.all([
          axios.get(`${config.apiBaseUrl}/equipment/`, { headers }),
          axios.get(`${config.apiBaseUrl}/maintenance-logs/`, { headers }),
        ]);
        setEquipment(equipResp.data);
        setLogs(logsResp.data);
      } catch (err) {
        console.error(err);
        setError(err);
      }
    }
    loadData();
  }, [getAccessTokenSilently]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Equipment
      </Typography>
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error loading equipment: {error.message}
        </Typography>
      )}
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>
            Equipment List
          </Typography>
          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Location</TableCell>
                  <TableCell>Use Range</TableCell>
                  <TableCell>In Use</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {equipment.map((item) => (
                  <TableRow key={item.id} hover>
                    <TableCell>{item.id}</TableCell>
                    <TableCell>{item.equipment_name}</TableCell>
                    <TableCell>
                      {item.location?.location_type} {item.location?.room_number}
                    </TableCell>
                    <TableCell>
                      {item.min_use_range} – {item.max_use_range}
                    </TableCell>
                    <TableCell>{item.in_use ? 'Yes' : 'No'}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>
        <Grid item xs={12} md={6}>
          <Typography variant="h6" gutterBottom>
            Maintenance Logs
          </Typography>
          <TableContainer component={Paper}>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Equipment</TableCell>
                  <TableCell>Service Date</TableCell>
                  <TableCell>Next Service</TableCell>
                  <TableCell>Interval</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {logs.map((log) => (
                  <TableRow key={log.id} hover>
                    <TableCell>{log.id}</TableCell>
                    <TableCell>{log.equipment?.equipment_name}</TableCell>
                    <TableCell>{log.service_date}</TableCell>
                    <TableCell>{log.next_service_date}</TableCell>
                    <TableCell>{log.service_interval}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Grid>
      </Grid>
    </Box>
  );
}

export default EquipmentPage;
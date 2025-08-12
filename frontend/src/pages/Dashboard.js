import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth0 } from '@auth0/auth0-react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import config from '../config';

// Register the Chart.js components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

/**
 * Dashboard page showing aggregated metrics and charts.
 */
function Dashboard() {
  const { getAccessTokenSilently } = useAuth0();
  const [warehouseData, setWarehouseData] = useState([]);
  const [versionChangeData, setVersionChangeData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const token = await getAccessTokenSilently();
        const headers = {
          Authorization: `Bearer ${token}`,
        };
        // Fetch warehouse clients aggregated data
        const warehouseResp = await axios.get(
          `${config.apiBaseUrl}/dashboard/warehouse-clients/`,
          { headers }
        );
        setWarehouseData(warehouseResp.data);
        // Fetch version change aggregated data
        const versionResp = await axios.get(
          `${config.apiBaseUrl}/dashboard/version-changes/`,
          { headers }
        );
        setVersionChangeData(versionResp.data);
      } catch (err) {
        console.error(err);
        setError(err);
      }
    }
    fetchData();
  }, [getAccessTokenSilently]);

  const warehouseChartData = {
    labels: warehouseData.map((item) => item.warehouse_facility),
    datasets: [
      {
        label: 'Number of Clients',
        data: warehouseData.map((item) => item.total_clients),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
    ],
  };

  const versionChartData = {
    labels: versionChangeData.map((item) => item.sop_name),
    datasets: [
      {
        label: 'Avg Days Between Effective Dates',
        data: versionChangeData.map((item) => item.average_days_between_effective_dates),
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };

  return (
    <Box sx={{ p: 3 }}>
      <Card sx={{ mb: 4, overflow: 'hidden' }}>
        <Box
          sx={{
            position: 'relative',
            height: { xs: 200, md: 300 },
            backgroundImage: `url(/hero.png)`,
            backgroundSize: 'cover',
            backgroundPosition: 'center',
          }}
        >
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              backgroundColor: 'rgba(0,0,0,0.3)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Typography variant="h3" color="white" sx={{ textAlign: 'center', px: 2 }}>
              Laboratory Information Management
            </Typography>
          </Box>
        </Box>
      </Card>
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error loading data: {error.message}
        </Typography>
      )}
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Clients Served per Warehouse
              </Typography>
              <Bar data={warehouseChartData} options={{ responsive: true, plugins: { legend: { display: false }, title: { display: false } } }} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Average Days Between SOP Effective Dates
              </Typography>
              <Bar data={versionChartData} options={{ responsive: true, plugins: { legend: { display: false }, title: { display: false } } }} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard;
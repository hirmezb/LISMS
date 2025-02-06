import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Samples() {
  const [samples, setSamples] = useState([]);
  const [newSample, setNewSample] = useState({
    product_name: '',
    product_stage: '',
    quantity: '',
    location_id: '',
    warehouse_id: '',
  });
  const [editingSampleId, setEditingSampleId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    fetchSamples();
  }, [currentPage, searchTerm]);

  const fetchSamples = async () => {
    try {
      const response = await axios.get(`/api/samples/?page=${currentPage}&search=${searchTerm}`);
      console.log('API Response:', response.data);

      if (Array.isArray(response.data)) {
        setSamples(response.data);
      } else if (response.data.results) {
        setSamples(response.data.results);
      } else {
        setSamples([]);
      }
    } catch (error) {
      console.error('Error fetching samples:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewSample((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let response;
      if (editingSampleId) {
        response = await axios.put(`/api/samples/${editingSampleId}/`, newSample);
        setSamples((prev) =>
          prev.map((sample) => (sample.id === editingSampleId ? response.data : sample))
        );
      } else {
        response = await axios.post('/api/samples/', newSample);
        setSamples((prev) => [response.data, ...prev]);
      }
      setNewSample({ product_name: '', product_stage: '', quantity: '', location_id: '', warehouse_id: '' });
      setEditingSampleId(null);
    } catch (error) {
      console.error('Error adding/updating sample:', error);
    }
  };

  const handleEdit = (sample) => {
    setEditingSampleId(sample.id);
    setNewSample(sample);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/samples/${id}/`);
      setSamples((prev) => prev.filter((sample) => sample.id !== id));
    } catch (error) {
      console.error('Error deleting sample:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const totalPages = Math.ceil(samples.length / itemsPerPage);

  return (
    <div className="page-container">
      <h1 className="page-title">Samples Management</h1>

      <input
        type="text"
        placeholder="Search Samples..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-bar"
      />

      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          name="product_name"
          placeholder="Product Name"
          value={newSample.product_name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="product_stage"
          placeholder="Product Stage"
          value={newSample.product_stage}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="quantity"
          placeholder="Quantity"
          value={newSample.quantity}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="location_id"
          placeholder="Location ID"
          value={newSample.location_id}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="warehouse_id"
          placeholder="Warehouse ID"
          value={newSample.warehouse_id}
          onChange={handleChange}
          required
        />
        <button type="submit">{editingSampleId ? 'Update Sample' : 'Register Sample'}</button>
      </form>

      <table className="data-table">
        <thead>
          <tr>
            <th>Product Name</th>
            <th>Product Stage</th>
            <th>Quantity</th>
            <th>Location ID</th>
            <th>Warehouse ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {samples.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage).map((sample) => (
            <tr key={sample.id}>
              <td>{sample.product_name}</td>
              <td>{sample.product_stage}</td>
              <td>{sample.quantity}</td>
              <td>{sample.location_id}</td>
              <td>{sample.warehouse_id}</td>
              <td>
                <button onClick={() => handleEdit(sample)}>Edit</button>
                <button onClick={() => handleDelete(sample.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div className="pagination">
        {Array.from({ length: totalPages }, (_, i) => (
          <button
            key={i + 1}
            onClick={() => setCurrentPage(i + 1)}
            className={currentPage === i + 1 ? 'active' : ''}
          >
            {i + 1}
          </button>
        ))}
      </div>
    </div>
  );
}

export default Samples;

import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Equipment() {
  const [equipment, setEquipment] = useState([]);
  const [newEquipment, setNewEquipment] = useState({
    equipment_name: '',
    min_use_range: '',
    max_use_range: '',
    in_use: false,
    location_id: '',
    sop_id: '',
  });
  const [editingId, setEditingId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    fetchEquipment();
  }, [currentPage, searchTerm]);

  const fetchEquipment = async () => {
    try {
      const response = await axios.get(`/api/equipment/?page=${currentPage}&search=${searchTerm}`);
      console.log('API Response:', response.data);

      if (Array.isArray(response.data)) {
        setEquipment(response.data);
      } else if (response.data.results) {
        setEquipment(response.data.results);
      } else {
        setEquipment([]);
      }
    } catch (error) {
      console.error('Error fetching equipment:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewEquipment((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let response;
      if (editingId) {
        response = await axios.put(`/api/equipment/${editingId}/`, newEquipment);
        setEquipment((prev) =>
          prev.map((item) => (item.id === editingId ? response.data : item))
        );
      } else {
        response = await axios.post('/api/equipment/', newEquipment);
        setEquipment((prev) => [response.data, ...prev]);
      }
      setNewEquipment({ equipment_name: '', min_use_range: '', max_use_range: '', in_use: false, location_id: '', sop_id: '' });
      setEditingId(null);
    } catch (error) {
      console.error('Error adding/updating equipment:', error);
    }
  };

  const handleEdit = (item) => {
    setEditingId(item.id);
    setNewEquipment(item);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/equipment/${id}/`);
      setEquipment((prev) => prev.filter((item) => item.id !== id));
    } catch (error) {
      console.error('Error deleting equipment:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const totalPages = Math.ceil(equipment.length / itemsPerPage);

  return (
    <div className="page-container">
      <h1 className="page-title">Equipment Management</h1>

      <input
        type="text"
        placeholder="Search Equipment..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-bar"
      />

      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          name="equipment_name"
          placeholder="Equipment Name"
          value={newEquipment.equipment_name}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="min_use_range"
          placeholder="Min Use Range"
          value={newEquipment.min_use_range}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="max_use_range"
          placeholder="Max Use Range"
          value={newEquipment.max_use_range}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="location_id"
          placeholder="Location ID"
          value={newEquipment.location_id}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="sop_id"
          placeholder="SOP ID"
          value={newEquipment.sop_id}
          onChange={handleChange}
          required
        />
        <label>
          In Use:
          <input
            type="checkbox"
            name="in_use"
            checked={newEquipment.in_use}
            onChange={handleChange}
          />
        </label>
        <button type="submit">{editingId ? 'Update Equipment' : 'Register Equipment'}</button>
      </form>

      <table className="data-table">
        <thead>
          <tr>
            <th>Equipment Name</th>
            <th>Min Use Range</th>
            <th>Max Use Range</th>
            <th>Location ID</th>
            <th>SOP ID</th>
            <th>In Use</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {equipment.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage).map((item) => (
            <tr key={item.id}>
              <td>{item.equipment_name}</td>
              <td>{item.min_use_range}</td>
              <td>{item.max_use_range}</td>
              <td>{item.location_id}</td>
              <td>{item.sop_id}</td>
              <td>{item.in_use ? 'Yes' : 'No'}</td>
              <td>
                <button onClick={() => handleEdit(item)}>Edit</button>
                <button onClick={() => handleDelete(item.id)}>Delete</button>
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

export default Equipment;

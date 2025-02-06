import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Locations() {
  const [locations, setLocations] = useState([]);
  const [newLocation, setNewLocation] = useState({
    location_type: '',
    room_number: '',
  });
  const [editingId, setEditingId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    fetchLocations();
  }, [currentPage, searchTerm]);

  const fetchLocations = async () => {
    try {
      const response = await axios.get(`/api/locations/?page=${currentPage}&search=${searchTerm}`);
      console.log('API Response:', response.data);

      if (Array.isArray(response.data)) {
        setLocations(response.data);
      } else if (response.data.results) {
        setLocations(response.data.results);
      } else {
        setLocations([]);
      }
    } catch (error) {
      console.error('Error fetching locations:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewLocation((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let response;
      if (editingId) {
        response = await axios.put(`/api/locations/${editingId}/`, newLocation);
        setLocations((prev) =>
          prev.map((location) => (location.id === editingId ? response.data : location))
        );
      } else {
        response = await axios.post('/api/locations/', newLocation);
        setLocations((prev) => [response.data, ...prev]);
      }
      setNewLocation({ location_type: '', room_number: '' });
      setEditingId(null);
    } catch (error) {
      console.error('Error adding/updating location:', error);
    }
  };

  const handleEdit = (location) => {
    setEditingId(location.id);
    setNewLocation(location);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/locations/${id}/`);
      setLocations((prev) => prev.filter((location) => location.id !== id));
    } catch (error) {
      console.error('Error deleting location:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const totalPages = Math.ceil(locations.length / itemsPerPage);

  return (
    <div className="page-container">
      <h1 className="page-title">Locations Management</h1>

      <input
        type="text"
        placeholder="Search Locations..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-bar"
      />

      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          name="location_type"
          placeholder="Location Type"
          value={newLocation.location_type}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="room_number"
          placeholder="Room Number"
          value={newLocation.room_number}
          onChange={handleChange}
          required
        />
        <button type="submit">{editingId ? 'Update Location' : 'Register Location'}</button>
      </form>

      <table className="data-table">
        <thead>
          <tr>
            <th>Location Type</th>
            <th>Room Number</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {locations.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage).map((location) => (
            <tr key={location.id}>
              <td>{location.location_type}</td>
              <td>{location.room_number}</td>
              <td>
                <button onClick={() => handleEdit(location)}>Edit</button>
                <button onClick={() => handleDelete(location.id)}>Delete</button>
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

export default Locations;

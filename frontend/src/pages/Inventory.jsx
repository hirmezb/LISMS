import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [newItem, setNewItem] = useState({
    item_name: '',
    quantity: '',
    description: '',
    warehouse_id: '',
    location_id: '',
  });
  const [editingId, setEditingId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    fetchInventory();
  }, [currentPage, searchTerm]);

  const fetchInventory = async () => {
    try {
      const response = await axios.get(`/api/inventory/?page=${currentPage}&search=${searchTerm}`);
      console.log('API Response:', response.data);

      if (Array.isArray(response.data)) {
        setInventory(response.data);
      } else if (response.data.results) {
        setInventory(response.data.results);
      } else {
        setInventory([]);
      }
    } catch (error) {
      console.error('Error fetching inventory:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewItem((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let response;
      if (editingId) {
        response = await axios.put(`/api/inventory/${editingId}/`, newItem);
        setInventory((prev) =>
          prev.map((item) => (item.id === editingId ? response.data : item))
        );
      } else {
        response = await axios.post('/api/inventory/', newItem);
        setInventory((prev) => [response.data, ...prev]);
      }
      setNewItem({ item_name: '', quantity: '', description: '', warehouse_id: '', location_id: '' });
      setEditingId(null);
    } catch (error) {
      console.error('Error adding/updating item:', error);
    }
  };

  const handleEdit = (item) => {
    setEditingId(item.id);
    setNewItem(item);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/inventory/${id}/`);
      setInventory((prev) => prev.filter((item) => item.id !== id));
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const totalPages = Math.ceil(inventory.length / itemsPerPage);

  return (
    <div className="page-container">
      <h1 className="page-title">Inventory Management</h1>

      <input
        type="text"
        placeholder="Search Items..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-bar"
      />

      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          name="item_name"
          placeholder="Item Name"
          value={newItem.item_name}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="quantity"
          placeholder="Quantity"
          value={newItem.quantity}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="description"
          placeholder="Description"
          value={newItem.description}
          onChange={handleChange}
        />
        <input
          type="text"
          name="warehouse_id"
          placeholder="Warehouse ID"
          value={newItem.warehouse_id}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="location_id"
          placeholder="Location ID"
          value={newItem.location_id}
          onChange={handleChange}
          required
        />
        <button type="submit">{editingId ? 'Update Item' : 'Register Item'}</button>
      </form>

      <table className="data-table">
        <thead>
          <tr>
            <th>Item Name</th>
            <th>Quantity</th>
            <th>Description</th>
            <th>Warehouse ID</th>
            <th>Location ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {inventory.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage).map((item) => (
            <tr key={item.id}>
              <td>{item.item_name}</td>
              <td>{item.quantity}</td>
              <td>{item.description}</td>
              <td>{item.warehouse_id}</td>
              <td>{item.location_id}</td>
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

export default Inventory;

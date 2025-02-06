import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Tests() {
  const [tests, setTests] = useState([]);
  const [newTest, setNewTest] = useState({
    test_name: '',
    min_acceptable_result: '',
    max_acceptable_result: '',
    sample_id: '',
    test_result: '',
  });
  const [editingTestId, setEditingTestId] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    fetchTests();
  }, [currentPage, searchTerm]);

  const fetchTests = async () => {
    try {
      const response = await axios.get(`/api/tests/?page=${currentPage}&search=${searchTerm}`);
      console.log('API Response:', response.data);

      if (Array.isArray(response.data)) {
        setTests(response.data);
      } else if (response.data.results) {
        setTests(response.data.results);
      } else {
        setTests([]);
      }
    } catch (error) {
      console.error('Error fetching tests:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewTest((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let response;
      if (editingTestId) {
        response = await axios.put(`/api/tests/${editingTestId}/`, newTest);
        setTests((prev) =>
          prev.map((test) => (test.id === editingTestId ? response.data : test))
        );
      } else {
        response = await axios.post('/api/tests/', newTest);
        setTests((prev) => [response.data, ...prev]);
      }
      setNewTest({ test_name: '', min_acceptable_result: '', max_acceptable_result: '', sample_id: '', test_result: '' });
      setEditingTestId(null);
    } catch (error) {
      console.error('Error adding/updating test:', error);
    }
  };

  const handleEdit = (test) => {
    setEditingTestId(test.id);
    setNewTest(test);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`/api/tests/${id}/`);
      setTests((prev) => prev.filter((test) => test.id !== id));
    } catch (error) {
      console.error('Error deleting test:', error);
    }
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
    setCurrentPage(1);
  };

  const totalPages = Math.ceil(tests.length / itemsPerPage);

  return (
    <div className="page-container">
      <h1 className="page-title">Tests Management</h1>

      <input
        type="text"
        placeholder="Search Tests..."
        value={searchTerm}
        onChange={handleSearch}
        className="search-bar"
      />

      <form onSubmit={handleSubmit} className="form">
        <input
          type="text"
          name="test_name"
          placeholder="Test Name"
          value={newTest.test_name}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="min_acceptable_result"
          placeholder="Min Acceptable Result"
          value={newTest.min_acceptable_result}
          onChange={handleChange}
        />
        <input
          type="number"
          name="max_acceptable_result"
          placeholder="Max Acceptable Result"
          value={newTest.max_acceptable_result}
          onChange={handleChange}
        />
        <input
          type="text"
          name="sample_id"
          placeholder="Sample ID"
          value={newTest.sample_id}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="test_result"
          placeholder="Test Result"
          value={newTest.test_result}
          onChange={handleChange}
          required
        />
        <button type="submit">{editingTestId ? 'Update Test' : 'Register Test'}</button>
      </form>

      <table className="data-table">
        <thead>
          <tr>
            <th>Test Name</th>
            <th>Min Acceptable Result</th>
            <th>Max Acceptable Result</th>
            <th>Sample ID</th>
            <th>Test Result</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tests.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage).map((test) => (
            <tr key={test.id}>
              <td>{test.test_name}</td>
              <td>{test.min_acceptable_result}</td>
              <td>{test.max_acceptable_result}</td>
              <td>{test.sample_id}</td>
              <td>{test.test_result}</td>
              <td>
                <button onClick={() => handleEdit(test)}>Edit</button>
                <button onClick={() => handleDelete(test.id)}>Delete</button>
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

export default Tests;

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [user, setUser] = useState({});
  const [formData, setFormData] = useState({ email: '', full_name: '' });

  useEffect(() => {
    axios.get('/users/me').then(response => {
      setUser(response.data);
      setFormData({ email: response.data.email, full_name: response.data.full_name });
    });
  }, []);

  const handleUpdate = () => {
    axios.put('/users/me', formData).then(response => {
      setUser(response.data);
      alert('Informations mises à jour');
    });
  };

  const handleDelete = () => {
    axios.delete('/users/me').then(() => {
      alert('Compte supprimé');
      // Rediriger ou effectuer une autre action
    });
  };

  return (
    <div>
      <h1>Bienvenue, {user.full_name}</h1>
      <input type="email" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} />
      <input type="text" value={formData.full_name} onChange={e => setFormData({ ...formData, full_name: e.target.value })} />
      <button onClick={handleUpdate}>Mettre à jour</button>
      <button onClick={handleDelete}>Supprimer le compte</button>
    </div>
  );
}

export default Dashboard;

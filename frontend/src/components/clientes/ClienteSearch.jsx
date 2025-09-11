// ClienteSearch.jsx
import React, { useState } from 'react';

const ClienteSearch = ({ onSelectCliente }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    // Implement search logic here
  };

  return (
    <div>
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Buscar cliente..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit">Buscar</button>
      </form>
      {/* Search results would go here */}
    </div>
  );
};

export default ClienteSearch;
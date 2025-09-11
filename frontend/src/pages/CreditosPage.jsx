// pages/CreditosPage.jsx
import React, { useState, useEffect } from 'react';
import { creditosService } from '../services/creditosService';
import CreditoForm from '../components/creditos/CreditoForm';
import CreditoList from '../components/creditos/CreditoList';
import styles from './CreditosPage.module.css';

const CreditosPage = () => {
  const [creditos, setCreditos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingCredito, setEditingCredito] = useState(null);

  useEffect(() => {
    fetchCreditos();
  }, []);

  const fetchCreditos = async () => {
    try {
      setLoading(true);
      const response = await creditosService.getCreditos();
      setCreditos(response.data);
    } catch (err) {
      setError('Erro ao carregar créditos');
      console.error('Erro:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateCredito = async (creditoData) => {
    try {
      await creditosService.createCredito(creditoData);
      setShowForm(false);
      fetchCreditos(); // Recarregar a lista
      alert('Crédito criado com sucesso!');
    } catch (err) {
      setError('Erro ao criar crédito: ' + (err.response?.data?.message || err.message));
    }
  };

  const handleEditCredito = async (creditoData) => {
    try {
      await creditosService.updateCredito(editingCredito.id, creditoData);
      setEditingCredito(null);
      fetchCreditos();
      alert('Crédito atualizado com sucesso!');
    } catch (err) {
      setError('Erro ao atualizar crédito');
    }
  };

  const handleDeleteCredito = async (creditoId) => {
    if (window.confirm('Tem certeza que deseja eliminar este crédito?')) {
      try {
        await creditosService.deleteCredito(creditoId);
        fetchCreditos();
        alert('Crédito eliminado com sucesso!');
      } catch (err) {
        setError('Erro ao eliminar crédito');
      }
    }
  };

  const handleViewDetails = (credito) => {
    // Navegar para página de detalhes ou mostrar modal
    console.log('Ver detalhes:', credito);
  };

  if (loading) return <div>Carregando...</div>;

  return (
    <div className="creditos-page">
      <div className="page-header">
        <h1>Gestão de Créditos</h1>
        <button 
          onClick={() => setShowForm(true)} 
          className="btn-primary"
        >
          + Novo Crédito
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {showForm && (
        <div className="form-modal">
          <div className="modal-content">
            <h2>Criar Novo Crédito</h2>
            <CreditoForm 
              onSubmit={handleCreateCredito}
              onCancel={() => setShowForm(false)}
            />
          </div>
        </div>
      )}

      {editingCredito && (
        <div className="form-modal">
          <div className="modal-content">
            <h2>Editar Crédito</h2>
            <CreditoForm 
              onSubmit={handleEditCredito}
              initialData={editingCredito}
              isEditing={true}
              onCancel={() => setEditingCredito(null)}
            />
          </div>
        </div>
      )}

      <CreditoList 
        creditos={creditos}
        onEdit={setEditingCredito}
        onDelete={handleDeleteCredito}
        onViewDetails={handleViewDetails}
      />
    </div>
  );
};

export default CreditosPage;
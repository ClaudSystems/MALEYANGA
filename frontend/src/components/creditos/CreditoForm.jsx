// components/CreditoForm.jsx
import React, { useState } from 'react';
import ClienteSearch from './../clientes/ClienteSearch';

const CreditoForm = ({ onSubmit, initialData = {}, isEditing = false }) => {
  const [selectedCliente, setSelectedCliente] = useState(initialData.cliente || null);
  const [formData, setFormData] = useState({
    valor_creditado: initialData.valor_creditado || '',
    date_concecao: initialData.date_concecao || new Date().toISOString().split('T')[0],
    numero_do_credito: initialData.numero_do_credito || '',
    percentual_de_juros: initialData.percentual_de_juros || '',
    percentual_juros_de_demora: initialData.percentual_juros_de_demora || '0.000',
    numero_de_prestacoes: initialData.numero_de_prestacoes || '',
    periodicidade: initialData.periodicidade || 'mensal',
    forma_de_calculo: initialData.forma_de_calculo || 'pmt',
    reter_capital: initialData.reter_capital || false,
    estado: initialData.estado || 'Aberto'
  });
  const [error, setError] = useState(null);

  const handleClienteSelect = (cliente) => {
    setSelectedCliente(cliente);
    setError(null);
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!selectedCliente) {
      setError('Selecione um cliente primeiro');
      return;
    }

    const creditoData = {
      ...formData,
      cliente: selectedCliente.id,
      valor_creditado: parseFloat(formData.valor_creditado),
      percentual_de_juros: parseFloat(formData.percentual_de_juros),
      percentual_juros_de_demora: parseFloat(formData.percentual_juros_de_demora),
      numero_de_prestacoes: parseInt(formData.numero_de_prestacoes)
    };

    onSubmit(creditoData);
  };

  return (
    <div className="credito-form-container">
      {error && <div className="error-message">{error}</div>}

      <div className="section">
        <h2>Selecionar Cliente</h2>
        <ClienteSearch onClienteSelected={handleClienteSelect} />
        
        {selectedCliente && (
          <div className="selected-cliente">
            <strong>Cliente selecionado:</strong> {selectedCliente.nome}
            {selectedCliente.codigo && ` (Código: ${selectedCliente.codigo})`}
          </div>
        )}
      </div>

      {selectedCliente && (
        <form onSubmit={handleSubmit} className="credito-form">
          <div className="form-grid">
            {/* Campos do formulário (igual ao que tinhas) */}
            <div className="form-group">
              <label>Valor Creditado *</label>
              <input
                type="number"
                name="valor_creditado"
                value={formData.valor_creditado}
                onChange={handleInputChange}
                step="0.01"
                min="0"
                required
              />
            </div>

            <div className="form-group">
              <label>Número do Crédito *</label>
              <input
                type="text"
                name="numero_do_credito"
                value={formData.numero_do_credito}
                onChange={handleInputChange}
                required
              />
            </div>

            {/* ... outros campos ... */}
          </div>

          <div className="form-actions">
            <button type="submit" className="submit-btn">
              {isEditing ? 'Atualizar Crédito' : 'Criar Crédito'}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default CreditoForm;
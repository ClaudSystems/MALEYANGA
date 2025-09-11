// components/CreditoList.jsx
import React from 'react';

const CreditoList = ({ creditos, onEdit, onDelete, onViewDetails }) => {
  if (!creditos || creditos.length === 0) {
    return <div className="no-data">Nenhum crédito encontrado</div>;
  }

  return (
    <div className="credito-list">
      <table className="credito-table">
        <thead>
          <tr>
            <th>Número</th>
            <th>Cliente</th>
            <th>Valor</th>
            <th>Data Concessão</th>
            <th>Prestações</th>
            <th>Estado</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {creditos.map(credito => (
            <tr key={credito.id}>
              <td>{credito.numero_do_credito}</td>
              <td>{credito.cliente_nome}</td>
              <td>{credito.valor_creditado} MT</td>
              <td>{credito.date_concecao}</td>
              <td>{credito.numero_de_prestacoes}x</td>
              <td>
                <span className={`status-badge status-${credito.estado.toLowerCase()}`}>
                  {credito.estado}
                </span>
              </td>
              <td>
                <div className="action-buttons">
                  <button onClick={() => onViewDetails(credito)} className="btn-view">
                    Ver
                  </button>
                  <button onClick={() => onEdit(credito)} className="btn-edit">
                    Editar
                  </button>
                  <button onClick={() => onDelete(credito.id)} className="btn-delete">
                    Eliminar
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CreditoList;
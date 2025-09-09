import React from 'react';
import { useOutletContext } from 'react-router-dom';

const Dashboard = () => {
  const { showNotification } = useOutletContext();
  
  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">📊 Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="font-semibold text-gray-700">Total de Clientes</h3>
          <p className="text-3xl font-bold text-blue-600">152</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="font-semibold text-gray-700">Assinantes Ativos</h3>
          <p className="text-3xl font-bold text-green-600">89</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="font-semibold text-gray-700">Receita Mensal</h3>
          <p className="text-3xl font-bold text-purple-600">R$ 25.640,00</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
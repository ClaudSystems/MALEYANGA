// src/App.jsx
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Dashboard from './Dashboard';
import ClientesPage from './pages/ClientesPage';
import Layout from './components/shared/Layout'; // Importe o Layout
import './App.css';

// Componente para a Rota Protegida
const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('access_token');
    return token ? children : <Navigate to="/login" replace />;
};

// Componente principal da aplicação
function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Rota de Login (pública) */}
                <Route path="/login" element={<Login />} />

                {/* Rotas Protegidas com Layout */}
                <Route
                    path="/"
                    element={
                        <PrivateRoute>
                            <Layout />
                        </PrivateRoute>
                    }
                >
                    {/* Rotas filhas que serão renderizadas no Outlet do Layout */}
                    <Route index element={<Dashboard />} />
                    <Route path="dashboard" element={<Dashboard />} />
                    <Route path="clientes" element={<ClientesPage />} />
                    <Route path="assinantes" element={<div>Página de Assinantes</div>} />
                </Route>

                {/* Rota fallback para páginas não encontradas */}
                <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
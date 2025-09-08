// src/App.jsx

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

// Importa o componente de login
import Login from './Login';

// Importa o componente do dashboard (a nossa nova homepage profissional)
import Dashboard from './Dashboard';
import ClientesPage from './pages/ClientesPage'; // Importa a página de clientes

import './App.css';

// Componente para a Rota Protegida
const PrivateRoute = ({ children }) => {
    // Verifica se existe um token de acesso no localStorage
    const token = localStorage.getItem('access_token');

    // Se o token existir, permite o acesso aos "children" (o componente Dashboard)
    // Se não existir, redireciona o utilizador para a página de login
    return token ? children : <Navigate to="/login" replace />;
};

// Componente principal da aplicação que configura as rotas
function App() {
    return (
        <BrowserRouter>
            <Routes>
                {/* Rota de Login (pública) */}
                <Route path="/login" element={<Login />} />

                {/* Rota Protegida: / */}
                <Route
                    path="/"
                    element={
                        <PrivateRoute>
                            <Dashboard />
                        </PrivateRoute>
                    }
                />

                {/* Rota Protegida para Clientes */}
                <Route
                    path="/clientes"
                    element={
                        <PrivateRoute>
                            <ClientesPage />
                        </PrivateRoute>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
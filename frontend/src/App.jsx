// src/App.jsx
import React from 'react';
import { SnackbarProvider } from 'notistack';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Login from './Login';
import Dashboard from './Dashboard';
import ClientesPage from './pages/ClientesPage';
import CreditosPage from './pages/CreditosPage';
import Layout from './components/shared/Layout';
import ErrorBoundary from './components/shared/ErrorBoundary';
import './App.css';
import TaxasPage from './pages/TaxasPage';

// Criar o tema do Material-UI
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

// Componente para a Rota Protegida
const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" replace />;
};

// Componente principal da aplicação
function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <SnackbarProvider 
          maxSnack={3}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
        >
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<Login />} />
              
              {/* Rotas protegidas com Layout */}
              <Route 
                path="/" 
                element={
                  <PrivateRoute>
                    <Layout />
                  </PrivateRoute>
                }
              >
                <Route index element={<Dashboard />} />
                <Route path="dashboard" element={<Dashboard />} />
                <Route path="clientes" element={<ClientesPage />} />
                <Route path="creditos" element={<CreditosPage />} />
                <Route path="assinantes" element={<div>Página de Assinantes</div>} />
                <Route path="taxas" element={<TaxasPage />} />
              </Route>
              
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </BrowserRouter>
        </SnackbarProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
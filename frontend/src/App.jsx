import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Login from './Login';

// ⭐ NOVO: Componente para a página principal
const HomePage = () => {
    const [count, setCount] = useState(0)

    const handleLogout = () => {
        // Remove o token do localStorage
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        // Redireciona para o login
        window.location.reload();
    };

    return (
        <>
            <div>
                <a href="https://vite.dev" target="_blank">
                    <img src={viteLogo} className="logo" alt="Vite logo" />
                </a>
                <a href="https://react.dev" target="_blank">
                    <img src={reactLogo} className="logo react" alt="React logo" />
                </a>
            </div>
            <h1>Vite + React</h1>
            <div className="card">
                <button onClick={() => setCount((count) => count + 1)}>
                    count is {count}
                </button>
                <p>
                    Edit <code>src/App.jsx</code> and save to test HMR
                </p>
            </div>
            <p className="read-the-docs">
                Click on the Vite and React logos to learn more
            </p>

            <div style={{ marginTop: '50px', padding: '20px', borderTop: '1px solid #ccc' }}>
                <button
                    onClick={handleLogout}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: '#ff4444',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer'
                    }}
                >
                    Logout
                </button>
            </div>
        </>
    )
}

// ⭐ NOVO: Componente de Rota Protegida
const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('access_token');
    return token ? children : <Navigate to="/login" replace />;
};

// ⭐ PRINCIPAL: Lógica de Roteamento
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
                            <HomePage />
                        </PrivateRoute>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
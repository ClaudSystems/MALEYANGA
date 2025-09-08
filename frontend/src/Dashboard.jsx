// src/Dashboard.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';
import logoImage from './assets/images/logo.png';

const Dashboard = () => {
    const navigate = useNavigate();
    const userName = "João Silva";

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
    };

    const menus = [
        {
            nome: 'Gestão de Clientes',
            url: '/clientes',
            descricao: 'Crie, edite e visualize informações de clientes.',
            icon: '👥'
        },
        {
            nome: 'Gestão de Créditos',
            url: '/creditos',
            descricao: 'Gerencie pedidos de crédito, aprovações e pagamentos.',
            icon: '💰'
        },
        {
            nome: 'Relatórios',
            url: '/relatorios',
            descricao: 'Acesse relatórios e estatísticas da aplicação.',
            icon: '📊'
        },
    ];

    const handleMenuClick = (url) => {
        navigate(url);
    };

    return (
        <div className="dashboard-container">
            <header className="navbar">
                <div className="logo-section">
                    <img src={logoImage} alt="Logo" className="logo-img"/>
                    <div className="logo">Gestão de Crédito e Contabilidade</div>
                </div>
                <div className="user-info">
                    <div className="user-details">
                        <span className="user-name">{userName}</span>
                        <span className="user-role">Administrador</span>
                    </div>
                    <div className="user-avatar">
                        {userName.split(' ').map(n => n[0]).join('')}
                    </div>
                    <button onClick={handleLogout} className="logout-btn">
                        <span className="logout-text">Sair</span>
                        <span className="logout-icon">→</span>
                    </button>
                </div>
            </header>

            <main className="main-content">
                <div className="welcome-section">
                    <h1>Bem-vindo, {userName.split(' ')[0]}!</h1>
                    <p>O que gostaria de fazer hoje?</p>
                </div>

                <div className="menu-grid">
                    {menus.map((menu, index) => (
                        <div key={index} className="menu-card" onClick={() => handleMenuClick(menu.url)}>
                            <div className="card-icon">{menu.icon}</div>
                            <h3>{menu.nome}</h3>
                            <p>{menu.descricao}</p>
                            <div className="btn">
                                Acessar
                                <span className="btn-arrow">→</span>
                            </div>
                        </div>
                    ))}
                </div>
            </main>

            <footer className="dashboard-footer">
                <p>© 2023 Gestão de Crédito - Todos os direitos reservados</p>
            </footer>
        </div>
    );
};

export default Dashboard;
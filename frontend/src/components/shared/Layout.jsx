import React, { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import Notification from './Notification';

const Layout = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [notification, setNotification] = useState({
        show: false,
        message: '',
        type: ''
    });
    const location = useLocation();

    // Função para obter o título da página baseado na rota
    const getPageTitle = () => {
        const routeTitles = {
            '/dashboard': '📊 Dashboard',
            '/clientes': '👥 Gestão de Clientes',
            '/assinantes': '📝 Assinantes',
            '/': '📊 Dashboard'
        };
        
        return routeTitles[location.pathname] || 'Sistema de Gestão';
    };

    const showNotification = (message, type = 'success') => {
        setNotification({ show: true, message, type });
        setTimeout(() => setNotification({ show: false, message: '', type: '' }), 3000);
    };

    return (
        <div className="flex h-screen bg-gray-100">
            {/* Sidebar */}
            <Sidebar
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
            />

            {/* Conteúdo principal */}
            <div className="flex-1 flex flex-col overflow-hidden">
                {/* Header com título dinâmico */}
                <Header 
                    onMenuClick={() => setSidebarOpen(!sidebarOpen)}
                    pageTitle={getPageTitle()}
                />

                {/* Conteúdo da página */}
                <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
                    <div className="container mx-auto px-4 py-6">
                        <Outlet context={{ showNotification }} />
                    </div>
                </main>
            </div>

            {/* Notificação global */}
            <Notification
                show={notification.show}
                message={notification.message}
                type={notification.type}
                onClose={() => setNotification({ show: false, message: '', type: '' })}
            />
        </div>
    );
};

export default Layout;
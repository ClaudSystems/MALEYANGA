// Notification.jsx
const Notification = ({ message, type = 'info' }) => {
    return (
        <div className={`notification notification-${type}`}>
            {message}
        </div>
    );
};

export default Notification;
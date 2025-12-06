import React from 'react';
import './pagina_menu.css';

const pagina_menu = () => {
    return (

        <div className = "menu-container">
            <h1>Bienvenido</h1>

            <div className = "menu-grid">

                <div className = "menu-item">
                    <span className="icon-placeholder"></span>
                    <p>Reseñas de Profesores</p>
                </div>

                <div className="menu-item">
                    <span className="icon-placeholder"></span>
                    <p>Portal Estudiantil</p>
                </div>

                <div className="menu-item">
                    <span className="icon-placeholder"></span>
                    <p>Horarios y Calendarios</p>
                </div>

            </div>
        </div>
    );
};

export default pagina_menu;
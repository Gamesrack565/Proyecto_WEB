import React from 'react';
import './pagina_registro.css'; // <-- La importación de CSS ahora es local

function RegisterPage() {
  return (
    <div className="auth-container">
      {/* Icono de usuario */}
      <div className="user-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
      </div>
      
      <p>Ingresa un correo y contraseña validos para registrarte</p>
      
      <form className="auth-form">
        <label htmlFor="correo">Correo</label>
        <input type="email" id="correo" placeholder="correo@dominio.com" />
        
        <label htmlFor="password">Contraseña</label>
        <input type="password" id="password" placeholder="Mínimo 8 carácteres" />
        
        <button type="submit" className="btn btn-primary">Registrarme</button>
        <button type="button" className="btn btn-secondary">Ya tengo una cuenta</button>
      </form>
    </div>
  );
}

export default RegisterPage;
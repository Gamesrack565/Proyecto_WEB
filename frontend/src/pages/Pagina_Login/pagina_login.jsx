import React from 'react';
import './pagina_login.css'; // <-- Importante que esto esté activo

function LoginPage() {
  return (
    <div className='auth-container'>
      
      <div className="user-icon">
        <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
      </div>

      <form className='auth-form'>
        
        <label htmlFor='correo'>Correo</label>
        <input type='email' id='correo' placeholder='correo@dominio.com' />
        
        <label htmlFor='password'>Contrasena</label>
        <input type='password' id='password' placeholder='Ingrese la contraseña' />
        
        <button type='submit' className='btn btn-primary'>Entrar</button>

      </form>
    </div>
  );
}

export default LoginPage;
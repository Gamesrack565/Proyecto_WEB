import React from 'react';
import {Link} from 'react-router-dom';
import './pagina_home.css';

function HomePage() {
    return (
        <div className='homepage-container'>
            <header className='home-header'>
                <div className='logo'>[Nombre del proyecto]</div>
                <nav>
                    <Link to='/portal'>Portal Estudiantil</Link>
                    <Link to='/resenas'>Resenas de Prosefores</Link>
                    <Link to='/horarios'>Horarios y Calendarios</Link>
                </nav>
                <div className='auth-links'>
                    <Link to='/login' className='btn-link'>Iniciar Sesion</Link>
                    <Link to='/registro' className='btn-link btn-link-primary'>Registrarse</Link>
                </div>
            </header>

            <main>
                <section className='mision-vision'>
                    <div className='card'>
                        <h2>Mision</h2>
                        <p>Proveer a la comunidad estudiantil de la
                        ESCOM una plataforma digital
                        centralizada y colaborativa que facilite
                        la toma de decisiones académicas,
                        fomente el intercambio de
                        conocimiento y optimice la gestión de
                        recursos educativos, integrando
                        opiniones, materiales de estudio y
                        herramientas de planificación en un
                        solo lugar.</p>
                    </div>
                    <div className='card'>
                        <h2>Vision</h2>
                        <p>Ser la herramienta digital indispensable
                        y de referencia para la vida académica
                        de todos los estudiantes de la ESCOM,
                        reconocida por su fiabilidad, utilidad y
                        por fomentar una comunidad
                        estudiantil más conectada, informada y
                        exitosa.</p>
                    </div>
                </section>

                <section className="features">
          <div className="feature-card">
            <h3>Que tu voz sea escuchada</h3>
            <p>Si tienes alguna experiencia que quieras compartir sobre un profesor, este es el sitio adecuado.</p>
          </div>
          <div className="feature-card">
            <h3>Apoyo a la comunidad</h3>
            <p>Puedes consultar el portal estudiantil donde encontrarás apuntes, exámenes y prácticas.</p>
          </div>
          <div className="feature-card">
            <h3>Mantente al tanto</h3>
            <p>Contamos con calendarios y datos oficiales para que construyas tu horario.</p>
          </div>
        </section>
      </main>

      <footer className="home-footer">
        <p>Contáctanos: correo@dominio.com</p>
        <p>55 1122 3344</p>
      </footer>

    </div>
  );
}

export default HomePage;
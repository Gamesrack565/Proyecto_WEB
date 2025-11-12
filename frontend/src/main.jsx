import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import HomePage from './pages/Pagina_Home/pagina_home.jsx';
import RegisterPage from './pages/Pagina_Registro/pagina_registro.jsx';
import LoginPage from './pages/Pagina_Login/pagina_login.jsx';

const router=createBrowserRouter([
  {
    path: '/',
    element:<App />,
    children: [
      {
        index:true,
        element:<HomePage />,
      },
      {
        index:true,
        element:<RegisterPage />,
      },
      {
        path:'login',
        element: <LoginPage />,
      },
    ],
  },
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
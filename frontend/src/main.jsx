import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import HomePage from './pages/Pagina_Home/pagina_home.jsx';
import RegisterPage from './pages/Pagina_Registro/pagina_registro.jsx';
import LoginPage from './pages/Pagina_Login/pagina_login.jsx';
import MenuPage from './pages/Pagina_Menu/pagina_menu.jsx';

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
        path:'registro',
        element:<RegisterPage />,
      },
      {
        path:'login',
        element: <LoginPage />,
      },
      {
        path: 'menu',
        element: <MenuPage />,
      },
    ],
  },
]);

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
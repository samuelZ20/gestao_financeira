import { Link, Navigate, Route, Routes } from 'react-router-dom'
import RotaProtegida from './components/RotaProtegida'
import { useAuth } from './context/authContext'
import Extrato from './pages/Extrato'
import Login from './pages/Login'

export default function App() {
  const { estaLogado, sair } = useAuth()

  return (
    <>
      {estaLogado && (
        <nav style={{ display: 'flex', gap: 16, padding: '12px 24px' }}>
          <Link to="/extrato">Extrato</Link>
          {/* RF003: Sair descarta o token; a RotaProtegida leva para o login */}
          <button type="button" onClick={sair}>
            Sair
          </button>
        </nav>
      )}
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/extrato"
          element={
            <RotaProtegida>
              <Extrato />
            </RotaProtegida>
          }
        />
        <Route path="*" element={<Navigate to="/extrato" replace />} />
      </Routes>
    </>
  )
}
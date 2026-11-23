import { Link, Route, Routes } from 'react-router-dom'
import Extrato from './pages/Extrato'
import Hello from './pages/Hello'

export default function App() {
  return (
    <>
      <nav style={{ display: 'flex', gap: 16, padding: '12px 24px' }}>
        <Link to="/">Início</Link>
        <Link to="/extrato">Extrato</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Hello />} />
        <Route path="/extrato" element={<Extrato />} />
      </Routes>
    </>
  )
}

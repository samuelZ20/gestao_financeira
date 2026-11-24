// I_Login (RF002): formulário de entrada com e-mail e senha.
import { useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/authContext'

export default function Login() {
  const { estaLogado, entrar } = useAuth()
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  // Quem já está logado não precisa ver o login
  if (estaLogado) {
    return <Navigate to="/extrato" replace />
  }

  async function aoEnviar(evento: FormEvent) {
    evento.preventDefault() // impede o navegador de recarregar a página
    setErro('')
    setEnviando(true)
    try {
      await entrar(email, senha)
      navigate('/extrato')
    } catch (e) {
      // IE_LoginCredenciaisInvalidas: mesma mensagem para e-mail ou senha errados
      if (axios.isAxiosError(e) && e.response?.status === 401) {
        setErro('E-mail ou senha inválidos.')
      } else {
        setErro('Não foi possível falar com o servidor.')
      }
    } finally {
      setEnviando(false)
    }
  }

  return (
    <main style={{ maxWidth: 360, margin: '64px auto', padding: 24 }}>
      <h1>Meu Bolso</h1>
      <form onSubmit={aoEnviar} style={{ display: 'grid', gap: 12 }}>
        <label>
          E-mail
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Senha
          <input type="password" value={senha} onChange={(e) => setSenha(e.target.value)} required />
        </label>
        {erro && <p role="alert" style={{ color: 'crimson' }}>{erro}</p>}
        <button type="submit" disabled={enviando}>
          {enviando ? 'Entrando...' : 'Entrar no Meu Bolso'}
        </button>
      </form>
      <p>
        Não tem conta? <Link to="/cadastro">Criar conta</Link>
      </p>
    </main>
  )
}
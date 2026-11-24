// Guarda o token e entrega entrar/sair para todas as telas (RF002, RF003).
import { useState, type ReactNode } from 'react'
import { CHAVE_TOKEN } from '../api/api'
import { entrar as entrarNaApi } from '../features/acesso/services/acessoService'
import { AuthContext } from './authContext'

export function AuthProvider({ children }: { children: ReactNode }) {
  // Começa com o token que já estava guardado (assim apertar F5 não desloga)
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(CHAVE_TOKEN))

  async function entrar(email: string, senha: string) {
    const novoToken = await entrarNaApi(email, senha) // se der 401, o erro sobe para a tela
    localStorage.setItem(CHAVE_TOKEN, novoToken)
    setToken(novoToken)
  }

  // RF003: sair = descartar o token
  function sair() {
    localStorage.removeItem(CHAVE_TOKEN)
    setToken(null)
  }

  return (
    <AuthContext.Provider value={{ estaLogado: token !== null, entrar, sair }}>
      {children}
    </AuthContext.Provider>
  )
}
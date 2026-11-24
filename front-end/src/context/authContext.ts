// O "quadro de avisos" do login: qualquer tela pode perguntar quem está logado.
import { createContext, useContext } from 'react'

export type Auth = {
  estaLogado: boolean
  entrar: (email: string, senha: string) => Promise<void>
  sair: () => void
}

export const AuthContext = createContext<Auth | null>(null)

// Atalho para as telas: const { estaLogado, entrar, sair } = useAuth()
export function useAuth(): Auth {
  const auth = useContext(AuthContext)
  if (auth === null) {
    throw new Error('useAuth precisa estar dentro do <AuthProvider>')
  }
  return auth
}
import { api } from '../../../api/api'

type TokenResposta = {
  access_token: string
  token_type: string
}

// RF002: manda e-mail e senha e recebe o token
export async function entrar(email: string, senha: string): Promise<string> {
  const { data } = await api.post<TokenResposta>('/acesso/login', { email, senha })
  return data.access_token
}
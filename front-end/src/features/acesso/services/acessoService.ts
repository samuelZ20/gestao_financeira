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

export type CadastroForm = {
  nome: string
  email: string
  senha: string
  aceita_politica: boolean
}

// RF001: cria a conta (a API devolve 201 com id, nome e e-mail)
export async function cadastrar(form: CadastroForm): Promise<void> {
  await api.post('/acesso/cadastro', form)
}
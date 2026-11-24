import axios from 'axios'

// Onde o crachá (token JWT) fica guardado no navegador
export const CHAVE_TOKEN = 'meubolso.token'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// Antes de TODA requisição: se houver token guardado, manda no cabeçalho (NF011)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(CHAVE_TOKEN)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Depois de TODA resposta: 401 numa rota protegida = token vencido ou inválido.
// Apaga o token e manda para o login (RN17). O 401 do próprio login não entra aqui.
api.interceptors.response.use(
  (resposta) => resposta,
  (erro) => {
    const ehLogin = erro.config?.url === '/acesso/login'
    if (erro.response?.status === 401 && !ehLogin) {
      localStorage.removeItem(CHAVE_TOKEN)
      window.location.href = '/login'
    }
    return Promise.reject(erro)
  },
)
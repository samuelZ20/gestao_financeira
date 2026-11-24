import axios from 'axios'

// Transforma o erro da API em { campo, mensagem } para mostrar junto ao campo.
export function lerErroDaApi(erro: unknown): { campo: string | null; mensagem: string } {
  if (axios.isAxiosError(erro) && erro.response) {
    const detail = erro.response.data?.detail
    if (typeof detail === 'string') {
      return { campo: erro.response.data?.campo ?? null, mensagem: detail }
    }
    if (Array.isArray(detail) && detail.length > 0) {
      // erro de validação do FastAPI: { loc: ['body', 'valor'], msg: '...' }
      const primeiro = detail[0]
      const campo = primeiro.loc?.[primeiro.loc.length - 1] ?? null
      const mensagem =
        campo === 'valor'
          ? 'Informe um valor maior que zero.'
          : String(primeiro.msg).replace(/^Value error, /, '')
      return { campo, mensagem }
    }
  }
  return { campo: null, mensagem: 'Não foi possível falar com o servidor.' }
}

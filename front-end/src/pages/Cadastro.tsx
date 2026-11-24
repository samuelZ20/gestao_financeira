// I_Cadastro (RF001): criação de conta com nome, e-mail, senha e aceite da política.
import { useState, type FormEvent } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/authContext'
import { cadastrar, type CadastroForm } from '../features/acesso/services/acessoService'

// Um erro por campo: { email: 'Este e-mail já está cadastrado.' }
type Erros = Partial<Record<keyof CadastroForm, string>>

const FORM_VAZIO: CadastroForm = { nome: '', email: '', senha: '', aceita_politica: false }

// IE_CadastroCampoInvalido: as mesmas regras da API, conferidas antes de enviar
function validar(form: CadastroForm): Erros {
  const erros: Erros = {}
  if (form.nome.trim() === '') erros.nome = 'Informe o seu nome.'
  if (!/^\S+@\S+\.\S+$/.test(form.email)) erros.email = 'Informe um e-mail válido.'
  if (form.senha.length < 8) erros.senha = 'A senha precisa ter pelo menos 8 caracteres.' // RN16
  if (!form.aceita_politica) erros.aceita_politica = 'É preciso aceitar a política de privacidade.' // RN15
  return erros
}

export default function Cadastro() {
  const { estaLogado, entrar } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState<CadastroForm>(FORM_VAZIO)
  const [erros, setErros] = useState<Erros>({})
  const [erroGeral, setErroGeral] = useState('')
  const [enviando, setEnviando] = useState(false)

  if (estaLogado) {
    return <Navigate to="/extrato" replace />
  }

  // Atualiza um campo do formulário sem mexer nos outros
  function mudar<K extends keyof CadastroForm>(campo: K, valor: CadastroForm[K]) {
    setForm({ ...form, [campo]: valor })
  }

  async function aoEnviar(evento: FormEvent) {
    evento.preventDefault()
    setErroGeral('')

    const errosEncontrados = validar(form)
    setErros(errosEncontrados)
    if (Object.keys(errosEncontrados).length > 0) return // não envia com erro

    setEnviando(true)
    try {
      await cadastrar(form)
      await entrar(form.email, form.senha) // RF001: depois de criar, já entra no sistema
      navigate('/extrato')
    } catch (e) {
      if (axios.isAxiosError(e) && e.response?.status === 409) {
        setErros({ email: 'Este e-mail já está cadastrado.' }) // IE_CadastroEmailExistente (RN01)
      } else if (axios.isAxiosError(e) && e.response?.status === 422) {
        setErroGeral('Confira os dados informados.')
      } else {
        setErroGeral('Não foi possível falar com o servidor.')
      }
    } finally {
      setEnviando(false)
    }
  }

  return (
    <main style={{ maxWidth: 360, margin: '64px auto', padding: 24 }}>
      <h1>Criar conta</h1>
      <form onSubmit={aoEnviar} noValidate style={{ display: 'grid', gap: 12 }}>
        <label>
          Nome
          <input value={form.nome} onChange={(e) => mudar('nome', e.target.value)} />
        </label>
        {erros.nome && <small style={{ color: 'crimson' }}>{erros.nome}</small>}

        <label>
          E-mail
          <input type="email" value={form.email} onChange={(e) => mudar('email', e.target.value)} />
        </label>
        {erros.email && <small style={{ color: 'crimson' }}>{erros.email}</small>}

        <label>
          Senha
          <input type="password" value={form.senha} onChange={(e) => mudar('senha', e.target.value)} />
        </label>
        {erros.senha && <small style={{ color: 'crimson' }}>{erros.senha}</small>}

        <label>
          <input
            type="checkbox"
            checked={form.aceita_politica}
            onChange={(e) => mudar('aceita_politica', e.target.checked)}
          />{' '}
          Li e aceito a política de privacidade
        </label>
        {erros.aceita_politica && <small style={{ color: 'crimson' }}>{erros.aceita_politica}</small>}

        {erroGeral && <p role="alert" style={{ color: 'crimson' }}>{erroGeral}</p>}
        <button type="submit" disabled={enviando}>
          {enviando ? 'Criando...' : 'Criar minha conta'}
        </button>
      </form>
      <p>
        Já tem conta? <Link to="/login">Entrar</Link>
      </p>
    </main>
  )
}
// I_FormularioCategoria (RF006 e RF008) e IE_CategoriaDuplicada.
import { useState } from 'react'
import { lerErroDaApi } from '../../lancamentos/services/erros'
import { alterarCategoria, cadastrarCategoria } from '../services/categoriasService'
import type { Categoria, CategoriaForm, Tipo } from '../types'

interface Props {
  categoria: Categoria | null // null = nova; preenchida = edição
  onSalvo: (mensagem: string) => void
  onCancelar: () => void
}

function formInicial(c: Categoria | null): CategoriaForm {
  return c ? { nome: c.nome, tipo: c.tipo } : { nome: '', tipo: 'despesa' }
}

export default function FormularioCategoria({ categoria, onSalvo, onCancelar }: Props) {
  const [form, setForm] = useState<CategoriaForm>(() => formInicial(categoria))
  // Erros por campo: { nome: '...', tipo: '...', geral: '...' }
  const [erros, setErros] = useState<Record<string, string>>({})
  const [salvando, setSalvando] = useState(false)

  function mudarTipo(tipo: Tipo) {
    setForm({ ...form, tipo })
  }

  // Conferência rápida no navegador, antes de chamar a API
  function validar(): Record<string, string> {
    const e: Record<string, string> = {}
    if (!form.nome.trim()) e.nome = 'Informe o nome.'
    return e
  }

  async function salvar(ev: React.FormEvent) {
    ev.preventDefault()
    const e = validar()
    setErros(e)
    if (Object.keys(e).length > 0) return

    const dados = { ...form, nome: form.nome.trim() }
    setSalvando(true)
    try {
      if (categoria) {
        await alterarCategoria(categoria.id, dados)
        onSalvo('Categoria alterada com sucesso!')
      } else {
        await cadastrarCategoria(dados)
        onSalvo('Categoria cadastrada com sucesso!')
      }
    } catch (erro) {
      // A API diz qual campo errou: "nome" (RN21, nome repetido), "tipo" (RN14,
      // categoria em uso) ou nenhum (ex.: 403 padrão, 404) -> mostra embaixo, em "geral".
      const { campo, mensagem } = lerErroDaApi(erro)
      setErros({ [campo ?? 'geral']: mensagem })
    } finally {
      setSalvando(false)
    }
  }

  return (
    <div className="modal-fundo" role="dialog" aria-modal="true">
      <form className="modal" onSubmit={salvar} noValidate>
        <h2>{categoria ? 'Editar categoria' : 'Nova categoria'}</h2>

        <label className="campo">
          <span>Nome</span>
          <input
            maxLength={50}
            value={form.nome}
            onChange={(e) => setForm({ ...form, nome: e.target.value })}
            autoFocus
          />
          {erros.nome && <small className="erro">{erros.nome}</small>}
        </label>

        <div className="campo">
          <span>Tipo</span>
          <div className="alternar">
            <button
              type="button"
              className={form.tipo === 'despesa' ? 'ativo' : ''}
              onClick={() => mudarTipo('despesa')}
            >
              Despesa
            </button>
            <button
              type="button"
              className={form.tipo === 'receita' ? 'ativo' : ''}
              onClick={() => mudarTipo('receita')}
            >
              Receita
            </button>
          </div>
          {erros.tipo && <small className="erro">{erros.tipo}</small>}
        </div>

        {erros.geral && <p className="erro">{erros.geral}</p>}

        <div className="acoes">
          <button type="button" className="secundario" onClick={onCancelar}>
            Cancelar
          </button>
          <button type="submit" disabled={salvando}>
            {salvando ? 'Salvando…' : 'Salvar categoria'}
          </button>
        </div>
      </form>
    </div>
  )
}

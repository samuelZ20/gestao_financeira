// I_NovoLancamento (RF010 e RF012) e IE_LancamentoValorInvalido.
import { useEffect, useState } from 'react'
import { hojeISO } from '../../../shared/utils/formatters'
import { lerErroDaApi } from '../services/erros'
import {
  alterarLancamento,
  listarCategorias,
  registrarLancamento,
} from '../services/lancamentosService'
import type { Categoria, Lancamento, LancamentoForm } from '../types'

interface Props {
  lancamento: Lancamento | null // null = novo; preenchido = edição
  onSalvo: (mensagem: string) => void
  onCancelar: () => void
}

function formInicial(l: Lancamento | null): LancamentoForm {
  if (!l) {
    return { tipo: 'despesa', descricao: '', valor: '', data: hojeISO(), categoria_id: null }
  }
  return {
    tipo: l.tipo,
    descricao: l.descricao,
    valor: l.valor,
    data: l.data,
    categoria_id: l.categoria.id,
  }
}

export default function NovoLancamentoModal({ lancamento, onSalvo, onCancelar }: Props) {
  const [form, setForm] = useState<LancamentoForm>(() => formInicial(lancamento))
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [erros, setErros] = useState<Record<string, string>>({})
  const [salvando, setSalvando] = useState(false)

  // RN02: só aparecem as categorias do tipo escolhido.
  useEffect(() => {
    listarCategorias(form.tipo).then(setCategorias).catch(() => setCategorias([]))
  }, [form.tipo])

  function mudarTipo(tipo: LancamentoForm['tipo']) {
    setForm({ ...form, tipo, categoria_id: null })
  }

  function validar(): Record<string, string> {
    const e: Record<string, string> = {}
    const valor = Number(form.valor.replace(',', '.'))
    if (!form.valor.trim() || !(valor > 0)) e.valor = 'Informe um valor maior que zero.'
    if (!form.descricao.trim()) e.descricao = 'A descrição é obrigatória.'
    if (!form.categoria_id) e.categoria_id = 'Escolha uma categoria.'
    return e
  }

  async function salvar(ev: React.FormEvent) {
    ev.preventDefault()
    const e = validar()
    setErros(e)
    if (Object.keys(e).length > 0) return

    setSalvando(true)
    try {
      if (lancamento) {
        await alterarLancamento(lancamento.id, form)
        onSalvo('Lançamento alterado com sucesso!')
      } else {
        await registrarLancamento(form)
        onSalvo('Lançamento registrado com sucesso!')
      }
    } catch (erro) {
      const { campo, mensagem } = lerErroDaApi(erro)
      setErros({ [campo ?? 'geral']: mensagem })
    } finally {
      setSalvando(false)
    }
  }

  return (
    <div className="modal-fundo" role="dialog" aria-modal="true">
      <form className="modal" onSubmit={salvar} noValidate>
        <h2>{lancamento ? 'Editar transação' : 'Nova transação'}</h2>

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
        </div>

        <label className="campo">
          <span>Descrição</span>
          <input
            maxLength={150}
            value={form.descricao}
            onChange={(e) => setForm({ ...form, descricao: e.target.value })}
          />
          {erros.descricao && <small className="erro">{erros.descricao}</small>}
        </label>

        <label className="campo">
          <span>Valor (R$)</span>
          <input
            inputMode="decimal"
            placeholder="0,00"
            value={form.valor}
            onChange={(e) => setForm({ ...form, valor: e.target.value })}
          />
          {erros.valor && <small className="erro">{erros.valor}</small>}
        </label>

        <label className="campo">
          <span>Data</span>
          <input
            type="date"
            value={form.data}
            onChange={(e) => setForm({ ...form, data: e.target.value })}
          />
        </label>

        <label className="campo">
          <span>Categoria</span>
          <select
            value={form.categoria_id ?? ''}
            onChange={(e) =>
              setForm({ ...form, categoria_id: e.target.value ? Number(e.target.value) : null })
            }
          >
            <option value="">Selecione…</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.id}>
                {c.nome}
              </option>
            ))}
          </select>
          {erros.categoria_id && <small className="erro">{erros.categoria_id}</small>}
        </label>

        {erros.geral && <p className="erro">{erros.geral}</p>}

        <div className="acoes">
          <button type="button" className="secundario" onClick={onCancelar}>
            Cancelar
          </button>
          <button type="submit" disabled={salvando}>
            {salvando ? 'Salvando…' : 'Salvar transação'}
          </button>
        </div>
      </form>
    </div>
  )
}

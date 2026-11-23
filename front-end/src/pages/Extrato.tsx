// I_Extrato (RF011, RF012, RF013): lista os lançamentos do mês.
import { useEffect, useState } from 'react'
import { formatCurrency, formatDate } from '../shared/utils/formatters'
import ConfirmacaoExclusao from '../features/lancamentos/components/ConfirmacaoExclusao'
import NovoLancamentoModal from '../features/lancamentos/components/NovoLancamentoModal'
import { useExtrato } from '../features/lancamentos/hooks/useExtrato'
import { lerErroDaApi } from '../features/lancamentos/services/erros'
import {
  excluirLancamento,
  listarCategorias,
} from '../features/lancamentos/services/lancamentosService'
import type { Categoria, FiltrosExtrato, Lancamento } from '../features/lancamentos/types'
import '../features/lancamentos/lancamentos.css'

const MSG_GERADO_POR_CONTA =
  'Este lançamento foi gerado por uma conta a pagar. Altere pela tela de Contas a pagar.'

function mesAtual(): string {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}

export default function Extrato() {
  const [mes, setMes] = useState(mesAtual()) // formato "AAAA-MM"
  const [tipo, setTipo] = useState<FiltrosExtrato['tipo']>('')
  const [categoriaId, setCategoriaId] = useState<number | ''>('')
  const [categorias, setCategorias] = useState<Categoria[]>([])

  const [editando, setEditando] = useState<Lancamento | null>(null)
  const [abrirModal, setAbrirModal] = useState(false)
  const [excluindo, setExcluindo] = useState<Lancamento | null>(null)
  const [aviso, setAviso] = useState<{ texto: string; erro: boolean } | null>(null)

  const [ano, numeroMes] = mes.split('-').map(Number)
  const { extrato, carregando, erro, recarregar } = useExtrato({
    ano,
    mes: numeroMes,
    tipo,
    categoria_id: categoriaId,
  })

  useEffect(() => {
    listarCategorias().then(setCategorias).catch(() => setCategorias([]))
  }, [])

  function abrirNovo() {
    setEditando(null)
    setAbrirModal(true)
  }

  function abrirEdicao(l: Lancamento) {
    if (l.gerado_por_conta) {
      setAviso({ texto: MSG_GERADO_POR_CONTA, erro: true }) // RN10
      return
    }
    setEditando(l)
    setAbrirModal(true)
  }

  function pedirExclusao(l: Lancamento) {
    if (l.gerado_por_conta) {
      setAviso({ texto: MSG_GERADO_POR_CONTA, erro: true }) // RN10
      return
    }
    setExcluindo(l)
  }

  function aoSalvar(mensagem: string) {
    setAbrirModal(false)
    setEditando(null)
    setAviso({ texto: mensagem, erro: false })
    recarregar()
  }

  async function confirmarExclusao() {
    if (!excluindo) return
    try {
      await excluirLancamento(excluindo.id)
      setAviso({ texto: 'Lançamento excluído com sucesso!', erro: false })
      recarregar()
    } catch (e) {
      setAviso({ texto: lerErroDaApi(e).mensagem, erro: true })
    } finally {
      setExcluindo(null)
    }
  }

  return (
    <main className="extrato">
      <header className="extrato-topo">
        <h1>Extrato</h1>
        <button type="button" onClick={abrirNovo}>
          + Nova transação
        </button>
      </header>

      {aviso && (
        <p className={aviso.erro ? 'aviso aviso-erro' : 'aviso aviso-ok'} role="status">
          {aviso.texto}
        </p>
      )}

      <section className="filtros">
        <label>
          Mês
          <input type="month" value={mes} onChange={(e) => e.target.value && setMes(e.target.value)} />
        </label>
        <label>
          Tipo
          <select value={tipo} onChange={(e) => setTipo(e.target.value as FiltrosExtrato['tipo'])}>
            <option value="">Tudo</option>
            <option value="receita">Entradas</option>
            <option value="despesa">Saídas</option>
          </select>
        </label>
        <label>
          Categoria
          <select
            value={categoriaId}
            onChange={(e) => setCategoriaId(e.target.value ? Number(e.target.value) : '')}
          >
            <option value="">Todas</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.id}>
                {c.nome}
              </option>
            ))}
          </select>
        </label>
      </section>

      {erro && <p className="aviso aviso-erro">{erro}</p>}
      {carregando && !extrato && <p>Carregando…</p>}

      {extrato && (
        <>
          <p className="resumo">
            {extrato.quantidade} lançamento(s) · Saldo do período:{' '}
            <strong className={Number(extrato.saldo_periodo) < 0 ? 'negativo' : 'positivo'}>
              {formatCurrency(extrato.saldo_periodo)}
            </strong>
          </p>

          {extrato.itens.length === 0 ? (
            <p className="vazio">Nenhum lançamento neste período.</p>
          ) : (
            <table className="tabela">
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Descrição</th>
                  <th>Categoria</th>
                  <th className="direita">Valor</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {extrato.itens.map((l) => (
                  <tr key={l.id}>
                    <td>{formatDate(l.data)}</td>
                    <td>
                      {l.descricao}
                      {l.gerado_por_conta && <span className="selo">conta paga</span>}
                    </td>
                    <td>{l.categoria.nome}</td>
                    <td className={l.tipo === 'receita' ? 'direita positivo' : 'direita negativo'}>
                      {l.tipo === 'receita' ? '+ ' : '− '}
                      {formatCurrency(l.valor)}
                    </td>
                    <td className="acoes-linha">
                      <button
                        type="button"
                        className="secundario"
                        disabled={l.gerado_por_conta}
                        title={l.gerado_por_conta ? MSG_GERADO_POR_CONTA : 'Editar'}
                        onClick={() => abrirEdicao(l)}
                      >
                        Editar
                      </button>
                      <button
                        type="button"
                        className="perigo"
                        disabled={l.gerado_por_conta}
                        title={l.gerado_por_conta ? MSG_GERADO_POR_CONTA : 'Excluir'}
                        onClick={() => pedirExclusao(l)}
                      >
                        Excluir
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}

      {abrirModal && (
        <NovoLancamentoModal
          lancamento={editando}
          onSalvo={aoSalvar}
          onCancelar={() => setAbrirModal(false)}
        />
      )}

      {excluindo && (
        <ConfirmacaoExclusao
          aviso={`Excluir "${excluindo.descricao}" (${formatCurrency(excluindo.valor)})? O saldo será recalculado.`}
          onConfirmar={confirmarExclusao}
          onCancelar={() => setExcluindo(null)}
        />
      )}
    </main>
  )
}

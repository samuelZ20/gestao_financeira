// I_Categorias (RF007, RF008, RF009): lista as categorias do usuário.
import { useEffect, useState } from 'react'
import FormularioCategoria from '../features/categorias/components/FormularioCategoria'
import { excluirCategoria, listarCategorias } from '../features/categorias/services/categoriasService'
import type { Categoria, Tipo } from '../features/categorias/types'
import ConfirmacaoExclusao from '../features/lancamentos/components/ConfirmacaoExclusao'
import { lerErroDaApi } from '../features/lancamentos/services/erros'
// Reaproveita o visual do Extrato (tabela, filtros, modal, avisos)
import '../features/lancamentos/lancamentos.css'

export default function Categorias() {
  const [tipo, setTipo] = useState<Tipo | ''>('') // '' = Tudo
  const [categorias, setCategorias] = useState<Categoria[]>([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState<string | null>(null)

  const [editando, setEditando] = useState<Categoria | null>(null)
  const [abrirFormulario, setAbrirFormulario] = useState(false)
  const [excluindo, setExcluindo] = useState<Categoria | null>(null)
  const [aviso, setAviso] = useState<{ texto: string; erro: boolean } | null>(null)

  const [recarga, setRecarga] = useState(0) // aumentar o número = buscar de novo

  // RF007: busca a lista ao abrir a tela, ao trocar o filtro e a cada recarregar().
  // Mesmo padrão do useExtrato: o estado só muda quando a resposta chega.
  useEffect(() => {
    let cancelado = false // evita mostrar a resposta de um filtro antigo
    listarCategorias(tipo || undefined)
      .then((dados) => {
        if (cancelado) return
        setCategorias(dados)
        setErro(null)
      })
      .catch((e) => {
        if (!cancelado) setErro(lerErroDaApi(e).mensagem)
      })
      .finally(() => {
        if (!cancelado) setCarregando(false)
      })
    return () => {
      cancelado = true
    }
  }, [tipo, recarga])

  const recarregar = () => setRecarga((n) => n + 1)

  function abrirNova() {
    setEditando(null)
    setAbrirFormulario(true)
  }

  function abrirEdicao(c: Categoria) {
    setEditando(c)
    setAbrirFormulario(true)
  }

  function aoSalvar(mensagem: string) {
    setAbrirFormulario(false)
    setEditando(null)
    setAviso({ texto: mensagem, erro: false })
    recarregar()
  }

  // RF009. Se a categoria estiver em uso, a API responde 409 (RN04, IE_CategoriaEmUso)
  // e a mensagem dela aparece no aviso vermelho.
  async function confirmarExclusao() {
    if (!excluindo) return
    try {
      await excluirCategoria(excluindo.id)
      setAviso({ texto: 'Categoria excluída com sucesso!', erro: false })
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
        <h1>Categorias</h1>
        <button type="button" onClick={abrirNova}>
          + Nova categoria
        </button>
      </header>

      {aviso && (
        <p className={aviso.erro ? 'aviso aviso-erro' : 'aviso aviso-ok'} role="status">
          {aviso.texto}
        </p>
      )}

      <section className="filtros">
        <label>
          Tipo
          <select value={tipo} onChange={(e) => setTipo(e.target.value as Tipo | '')}>
            <option value="">Tudo</option>
            <option value="receita">Receitas</option>
            <option value="despesa">Despesas</option>
          </select>
        </label>
      </section>

      {erro && <p className="aviso aviso-erro">{erro}</p>}
      {carregando && categorias.length === 0 && <p>Carregando…</p>}

      {!carregando && !erro && categorias.length === 0 && (
        <p className="vazio">Nenhuma categoria encontrada.</p>
      )}

      {categorias.length > 0 && (
        <table className="tabela">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Tipo</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {categorias.map((c) => (
              <tr key={c.id}>
                <td>
                  {c.nome}
                  {/* RN22: criada automaticamente no cadastro */}
                  {c.padrao && <span className="selo">padrão</span>}
                </td>
                <td className={c.tipo === 'receita' ? 'positivo' : 'negativo'}>
                  {c.tipo === 'receita' ? 'Receita' : 'Despesa'}
                </td>
                <td className="acoes-linha">
                  {/* RN09: categoria padrão não tem Editar nem Excluir */}
                  {!c.padrao && (
                    <>
                      <button type="button" className="secundario" onClick={() => abrirEdicao(c)}>
                        Editar
                      </button>
                      <button type="button" className="perigo" onClick={() => setExcluindo(c)}>
                        Excluir
                      </button>
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {abrirFormulario && (
        <FormularioCategoria
          categoria={editando}
          onSalvo={aoSalvar}
          onCancelar={() => setAbrirFormulario(false)}
        />
      )}

      {excluindo && (
        <ConfirmacaoExclusao
          aviso={`Excluir a categoria ${excluindo.nome}?`}
          onConfirmar={confirmarExclusao}
          onCancelar={() => setExcluindo(null)}
        />
      )}
    </main>
  )
}

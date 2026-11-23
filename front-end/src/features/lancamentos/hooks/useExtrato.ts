import { useEffect, useState } from 'react'
import { listarLancamentos } from '../services/lancamentosService'
import type { Extrato, FiltrosExtrato } from '../types'

// Busca o extrato sempre que o mês ou os filtros mudam.
// Chame recarregar() depois de registrar, alterar ou excluir um lançamento.
export function useExtrato(filtros: FiltrosExtrato) {
  const [extrato, setExtrato] = useState<Extrato | null>(null)
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')
  const [recarga, setRecarga] = useState(0)

  const { ano, mes, tipo, categoria_id } = filtros

  useEffect(() => {
    let cancelado = false // evita atualizar a tela com uma resposta antiga
    listarLancamentos({ ano, mes, tipo, categoria_id })
      .then((dados) => {
        if (cancelado) return
        setExtrato(dados)
        setErro('')
      })
      .catch(() => {
        if (!cancelado) setErro('Não foi possível carregar o extrato.')
      })
      .finally(() => {
        if (!cancelado) setCarregando(false)
      })
    return () => {
      cancelado = true
    }
  }, [ano, mes, tipo, categoria_id, recarga])

  const recarregar = () => setRecarga((n) => n + 1)

  return { extrato, carregando, erro, recarregar }
}

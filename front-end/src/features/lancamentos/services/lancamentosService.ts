import { api } from '../../../api/api'
import type {
  Categoria,
  Extrato,
  FiltrosExtrato,
  Lancamento,
  LancamentoForm,
  Tipo,
} from '../types'

export async function listarLancamentos(filtros: FiltrosExtrato): Promise<Extrato> {
  const params: Record<string, string | number> = {
    ano: filtros.ano,
    mes: filtros.mes,
  }
  if (filtros.tipo) params.tipo = filtros.tipo
  if (filtros.categoria_id) params.categoria_id = filtros.categoria_id
  const { data } = await api.get<Extrato>('/lancamentos', { params })
  return data
}

function corpo(form: LancamentoForm) {
  return { ...form, valor: form.valor.replace(',', '.') }
}

export async function registrarLancamento(form: LancamentoForm): Promise<Lancamento> {
  const { data } = await api.post<Lancamento>('/lancamentos', corpo(form))
  return data
}

export async function alterarLancamento(
  id: number,
  form: LancamentoForm,
): Promise<Lancamento> {
  const { data } = await api.put<Lancamento>(`/lancamentos/${id}`, corpo(form))
  return data
}

export async function excluirLancamento(id: number): Promise<void> {
  await api.delete(`/lancamentos/${id}`)
}

export async function listarCategorias(tipo?: Tipo): Promise<Categoria[]> {
  const { data } = await api.get<Categoria[]>('/categorias', {
    params: tipo ? { tipo } : {},
  })
  return data
}

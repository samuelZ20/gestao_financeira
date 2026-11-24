// Chamadas HTTP do módulo Categorias. O `api` já manda o token em toda requisição.
import { api } from '../../../api/api'
import type { Categoria, CategoriaForm, Tipo } from '../types'

// RF007: sem tipo traz todas; com tipo traz só receitas ou só despesas
export async function listarCategorias(tipo?: Tipo): Promise<Categoria[]> {
  const { data } = await api.get<Categoria[]>('/categorias', {
    params: tipo ? { tipo } : {},
  })
  return data
}

// RF006: a API responde 201 com a categoria criada
export async function cadastrarCategoria(form: CategoriaForm): Promise<Categoria> {
  const { data } = await api.post<Categoria>('/categorias', form)
  return data
}

// RF008: a API responde 200 com a categoria alterada
export async function alterarCategoria(id: number, form: CategoriaForm): Promise<Categoria> {
  const { data } = await api.put<Categoria>(`/categorias/${id}`, form)
  return data
}

// RF009: a API responde 204, sem corpo
export async function excluirCategoria(id: number): Promise<void> {
  await api.delete(`/categorias/${id}`)
}

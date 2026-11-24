export type Tipo = 'receita' | 'despesa'

export interface Categoria {
  id: number
  nome: string
  tipo: Tipo
}

export interface Lancamento {
  id: number
  tipo: Tipo
  descricao: string
  valor: string
  data: string
  categoria: { id: number; nome: string }
  gerado_por_conta: boolean
}

export interface Extrato {
  itens: Lancamento[]
  quantidade: number
  saldo_periodo: string
}

export interface LancamentoForm {
  tipo: Tipo
  descricao: string
  valor: string
  data: string
  categoria_id: number | null
}

export interface FiltrosExtrato {
  ano: number
  mes: number
  tipo: Tipo | ''
  categoria_id: number | ''
}

export type Tipo = 'receita' | 'despesa'

// Como a API devolve cada categoria (GET /categorias)
export interface Categoria {
  id: number
  nome: string
  tipo: Tipo
  padrao: boolean // RN09/RN22: true = criada no cadastro; não pode ser editada nem excluída
}

// O que o formulário envia ao cadastrar (RF006) ou alterar (RF008)
export interface CategoriaForm {
  nome: string
  tipo: Tipo
}

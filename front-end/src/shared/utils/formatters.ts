// RN24: valores como R$ 1.234,56 e datas como DD/MM/AAAA.

export function formatCurrency(valor: number | string): string {
  return Number(valor).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

// A API manda a data como "2026-11-10". Não usamos new Date() para não
// sofrer com fuso horário (poderia mostrar o dia anterior).
export function formatDate(iso: string): string {
  const [ano, mes, dia] = iso.split('-')
  return `${dia}/${mes}/${ano}`
}

export function hojeISO(): string {
  const d = new Date()
  const mes = String(d.getMonth() + 1).padStart(2, '0')
  const dia = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${mes}-${dia}`
}

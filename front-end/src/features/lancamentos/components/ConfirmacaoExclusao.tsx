// I_ConfirmacaoExclusao (RF013). Será reutilizada nas outras exclusões.
interface Props {
  aviso: string
  onConfirmar: () => void
  onCancelar: () => void
}

export default function ConfirmacaoExclusao({ aviso, onConfirmar, onCancelar }: Props) {
  return (
    <div className="modal-fundo" role="dialog" aria-modal="true">
      <div className="modal">
        <h2>Confirmar exclusão</h2>
        <p>{aviso}</p>
        <div className="acoes">
          <button type="button" className="secundario" onClick={onCancelar}>
            Cancelar
          </button>
          <button type="button" className="perigo" onClick={onConfirmar}>
            Excluir
          </button>
        </div>
      </div>
    </div>
  )
}

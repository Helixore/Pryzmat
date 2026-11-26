export default function StateMessage({ kind, title, message, onRetry }) {
  return (
    <div className={`state state-${kind}`}>
      {kind === 'loading' && <div className="spinner" />}
      {kind === 'error' && <div className="state-icon">!</div>}
      {kind === 'empty' && <div className="state-icon">∅</div>}
      {title && <h3>{title}</h3>}
      {message && <p>{message}</p>}
      {onRetry && (
        <button className="btn btn-primary" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}

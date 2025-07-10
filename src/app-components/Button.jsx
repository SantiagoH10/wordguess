export const Button = ({ children, onClick, disabled = false }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`cursor-pointer rounded-lg border-b-[4px] border-red-600 bg-red-500 px-6 py-2 text-white transition-all hover:-translate-y-[1px] hover:border-b-[6px] hover:brightness-110 active:translate-y-[2px] active:border-b-[2px] active:brightness-90 ${disabled ? 'cursor-not-allowed opacity-50' : ''} `}
    >
      {children}
    </button>
  )
}

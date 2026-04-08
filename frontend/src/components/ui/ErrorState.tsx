interface ErrorStateProps {
  message: string;
}

export default function ErrorState({ message }: ErrorStateProps) {
  return <div className="state-card error">{message}</div>;
}

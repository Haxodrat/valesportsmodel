interface LoadingStateProps {
  label?: string;
}

export default function LoadingState({ label = 'Loading...' }: LoadingStateProps) {
  return <div className="state-card">{label}</div>;
}

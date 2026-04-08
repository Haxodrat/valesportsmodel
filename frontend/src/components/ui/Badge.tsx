import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  tone?: 'default' | 'accent' | 'success';
}

export default function Badge({ children, tone = 'default' }: BadgeProps) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

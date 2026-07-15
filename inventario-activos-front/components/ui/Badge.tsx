interface BadgeProps {
  text: string;
  variant?: "success" | "warning" | "danger" | "default";
}

const colors: Record<string, string> = {
  success: "bg-green-100 text-green-800",
  warning: "bg-yellow-100 text-yellow-800",
  danger: "bg-red-100 text-red-800",
  default: "bg-gray-100 text-gray-800",
};

export function Badge({ text, variant = "default" }: BadgeProps) {
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${colors[variant]}`}>
      {text}
    </span>
  );
}

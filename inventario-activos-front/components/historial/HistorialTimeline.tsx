"use client";

import { Badge } from "@/components/ui/Badge";

export interface Movimiento {
  id: number;
  ubicacion_anterior?: { nombre: string } | null;
  ubicacion_nueva?: { nombre: string } | null;
  custodio_anterior?: { nombre: string } | null;
  custodio_nuevo?: { nombre: string } | null;
  estado_anterior?: { nombre: string } | null;
  estado_nuevo?: { nombre: string } | null;
  motivo?: string | null;
  fecha_movimiento: string;
}

interface HistorialTimelineProps {
  movimientos: Movimiento[];
}

function cambiar({
  anterior,
  nuevo,
  label,
}: {
  anterior?: { nombre: string } | null;
  nuevo?: { nombre: string } | null;
  label: string;
}) {
  if (!anterior && !nuevo) return null;
  return (
    <p className="text-sm text-gray-700">
      {label}: <span className="text-gray-600">{anterior?.nombre ?? "(ninguno)"}</span>
      {" → "}
      <span className="font-medium">{nuevo?.nombre ?? "(ninguno)"}</span>
    </p>
  );
}

export function HistorialTimeline({ movimientos }: HistorialTimelineProps) {
  if (movimientos.length === 0) {
    return <p className="text-gray-600 text-sm">Sin movimientos registrados</p>;
  }
  return (
    <div className="space-y-4">
      {movimientos.map((m) => (
        <div key={m.id} className="border-l-2 border-blue-400 pl-4 py-2">
          <p className="text-xs text-gray-500 mb-1">
            {new Date(m.fecha_movimiento).toLocaleString("es-CO")}
          </p>
          {cambiar({ anterior: m.ubicacion_anterior, nuevo: m.ubicacion_nueva, label: "Ubicación" })}
          {cambiar({ anterior: m.custodio_anterior, nuevo: m.custodio_nuevo, label: "Custodio" })}
          {cambiar({ anterior: m.estado_anterior, nuevo: m.estado_nuevo, label: "Estado" })}
          {m.motivo && <p className="text-sm text-gray-600 mt-1">Motivo: {m.motivo}</p>}
        </div>
      ))}
    </div>
  );
}

"use client";

import { useState } from "react";

import { Button } from "@/components/ui/Button";

export interface UbicacionArbol {
  id: number;
  nombre: string;
  nivel?: string | null;
  hijos: UbicacionArbol[];
}

interface UbicacionTreeProps {
  nodos: UbicacionArbol[];
  onDelete: (id: number) => Promise<void>;
}

function UbicacionNodo({ nodo, onDelete }: { nodo: UbicacionArbol; onDelete: (id: number) => Promise<void> }) {
  const [expanded, setExpanded] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");
  const hasHijos = nodo.hijos.length > 0;

  const handleDelete = async () => {
    if (!confirm(`¿Desactivar "${nodo.nombre}"?`)) return;
    setDeleting(true);
    setError("");
    try {
      await onDelete(nodo.id);
    } catch (err: any) {
      setError(err.detail || "Error al desactivar");
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="ml-4 border-l pl-4 py-1">
      <div className="flex items-center gap-2">
        {hasHijos && (
          <button onClick={() => setExpanded(!expanded)} className="text-sm text-blue-600 hover:underline">
            {expanded ? "[-]" : "[+]"}
          </button>
        )}
        {!hasHijos && <span className="text-sm text-gray-500 w-6">-</span>}
        <span className="text-sm font-medium">{nodo.nombre}</span>
        {nodo.nivel && <span className="text-xs text-gray-600">({nodo.nivel})</span>}
        <Button variant="danger" type="button" onClick={handleDelete} loading={deleting} className="text-xs px-2 py-0.5">
          Eliminar
        </Button>
      </div>
      {error && <p className="text-red-500 text-xs ml-6">{error}</p>}
      {expanded && hasHijos && (
        <div>
          {nodo.hijos.map((hijo) => (
            <UbicacionNodo key={hijo.id} nodo={hijo} onDelete={onDelete} />
          ))}
        </div>
      )}
    </div>
  );
}

export function UbicacionTree({ nodos, onDelete }: UbicacionTreeProps) {
  if (nodos.length === 0) {
    return <p className="text-gray-500 text-sm">No hay ubicaciones activas</p>;
  }
  return (
    <div>
      {nodos.map((nodo) => (
        <UbicacionNodo key={nodo.id} nodo={nodo} onDelete={onDelete} />
      ))}
    </div>
  );
}

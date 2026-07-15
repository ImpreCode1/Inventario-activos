"use client";

import Link from "next/link";

import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Table } from "@/components/ui/Table";

export interface ActivoRow {
  id: number;
  codigo_interno: string;
  nombre: string;
  categoria?: { id: number; nombre: string };
  ubicacion?: { id: number; nombre: string } | null;
  custodio?: { id: number; nombre: string } | null;
  estado?: { id: number; nombre: string };
}

interface ActivosTableProps {
  data: ActivoRow[];
  skip: number;
  limit: number;
  onPrev: () => void;
  onNext: () => void;
  hasMore: boolean;
}

const badgeVariant: Record<string, "success" | "warning" | "danger" | "default"> = {
  Disponible: "success",
  Asignado: "default",
  "En mantenimiento": "warning",
  "Dado de baja": "danger",
};

export function ActivosTable({ data, skip, limit, onPrev, onNext, hasMore }: ActivosTableProps) {
  const columns = [
    { key: "codigo_interno", header: "Código" },
    { key: "nombre", header: "Nombre" },
    {
      key: "categoria",
      header: "Categoría",
      render: (row: ActivoRow) => row.categoria?.nombre ?? "-",
    },
    {
      key: "ubicacion",
      header: "Ubicación",
      render: (row: ActivoRow) => row.ubicacion?.nombre ?? "-",
    },
    {
      key: "custodio",
      header: "Custodio",
      render: (row: ActivoRow) => row.custodio?.nombre ?? "-",
    },
    {
      key: "estado",
      header: "Estado",
      render: (row: ActivoRow) => (
        <Badge text={row.estado?.nombre ?? "-"} variant={badgeVariant[row.estado?.nombre ?? ""] ?? "default"} />
      ),
    },
    {
      key: "acciones",
      header: "",
      render: (row: ActivoRow) => (
        <div className="flex gap-2">
          <Link href={`/activos/${row.id}`}>
            <Button variant="secondary" type="button">Ver</Button>
          </Link>
          <Link href={`/activos/${row.id}/editar`}>
            <Button variant="secondary" type="button">Editar</Button>
          </Link>
        </div>
      ),
    },
  ];

  return (
    <div>
      <Table columns={columns} data={data} keyExtractor={(r: ActivoRow) => r.id} />
      <div className="flex justify-between items-center mt-4">
        <span className="text-sm text-gray-600">
          Mostrando {data.length > 0 ? skip + 1 : 0}–{skip + data.length}
        </span>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={onPrev} disabled={skip === 0}>
            Anterior
          </Button>
          <Button variant="secondary" onClick={onNext} disabled={!hasMore}>
            Siguiente
          </Button>
        </div>
      </div>
    </div>
  );
}

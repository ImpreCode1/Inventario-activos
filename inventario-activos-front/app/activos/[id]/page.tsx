"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";

import { api } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { ReasignarModal } from "@/components/activos/ReasignarModal";
import { HistorialTimeline, Movimiento } from "@/components/historial/HistorialTimeline";

interface ActivoDetail {
  id: number;
  codigo_interno: string;
  nombre: string;
  marca?: string | null;
  modelo?: string | null;
  serial?: string | null;
  valor?: number | null;
  categoria?: { id: number; nombre: string } | null;
  ubicacion?: { id: number; nombre: string } | null;
  custodio?: { id: number; nombre: string } | null;
  estado?: { id: number; nombre: string } | null;
  fecha_adquisicion?: string | null;
  observaciones?: string | null;
  created_at: string;
  updated_at: string;
  movimientos: Movimiento[];
}

interface SelectOption {
  value: string;
  label: string;
}

export default function ActivoDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [activo, setActivo] = useState<ActivoDetail | null>(null);
  const [error, setError] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [ubicaciones, setUbicaciones] = useState<SelectOption[]>([]);
  const [custodios, setCustodios] = useState<SelectOption[]>([]);
  const [estados, setEstados] = useState<SelectOption[]>([]);

  const load = () => {
    api.get<ActivoDetail>(`/api/v1/activos/${id}`)
      .then(setActivo)
      .catch((err) => setError(err.detail || "Error al cargar"));
  };

  useEffect(() => { load(); }, [id]);

  const openReasignar = async () => {
    try {
      const [ubis, usrs, ests] = await Promise.all([
        api.get<any[]>("/api/v1/ubicaciones"),
        api.get<any[]>("/api/v1/usuarios").catch(() => []),
        api.get<any[]>("/api/v1/estados_activo").catch(() => [
          { id: 1, nombre: "Disponible" }, { id: 2, nombre: "Asignado" },
          { id: 3, nombre: "En mantenimiento" }, { id: 4, nombre: "Dado de baja" },
        ]),
      ]);
      setUbicaciones(ubis.map((u) => ({ value: String(u.id), label: u.nombre })));
      setCustodios(usrs.map((u) => ({ value: String(u.id), label: u.nombre })));
      setEstados(ests.map((e) => ({ value: String(e.id), label: e.nombre })));
      setModalOpen(true);
    } catch (err: any) {
      setError(err.detail || "Error al cargar catálogos");
    }
  };

  const handleReasignar = async (body: Record<string, unknown>) => {
    await api.patch(`/api/v1/activos/${id}/reasignar`, body);
    load();
  };

  if (error) return <p className="text-red-500">{error}</p>;
  if (!activo) return <p>Cargando...</p>;

  const badgeVariant: Record<string, "success" | "warning" | "danger" | "default"> = {
    Disponible: "success", Asignado: "default",
    "En mantenimiento": "warning", "Dado de baja": "danger",
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">{activo.nombre}</h1>
        <div className="flex gap-2">
          <Link href={`/activos/${id}/editar`}><Button variant="secondary">Editar</Button></Link>
          <Button onClick={openReasignar}>Reasignar</Button>
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow mb-6 grid grid-cols-2 gap-4 text-sm">
        <div><span className="font-medium">Código:</span> {activo.codigo_interno}</div>
        <div><span className="font-medium">Marca:</span> {activo.marca ?? "-"}</div>
        <div><span className="font-medium">Modelo:</span> {activo.modelo ?? "-"}</div>
        <div><span className="font-medium">Serial:</span> {activo.serial ?? "-"}</div>
        <div><span className="font-medium">Valor:</span> {activo.valor ? `$${Number(activo.valor).toLocaleString("es-CO")}` : "-"}</div>
        <div><span className="font-medium">Categoría:</span> {activo.categoria?.nombre ?? "-"}</div>
        <div><span className="font-medium">Ubicación:</span> {activo.ubicacion?.nombre ?? "-"}</div>
        <div><span className="font-medium">Custodio:</span> {activo.custodio?.nombre ?? "-"}</div>
        <div>
          <span className="font-medium">Estado:</span>{" "}
          <Badge text={activo.estado?.nombre ?? "-"} variant={badgeVariant[activo.estado?.nombre ?? ""] ?? "default"} />
        </div>
        <div><span className="font-medium">Adquisición:</span> {activo.fecha_adquisicion ?? "-"}</div>
        <div className="col-span-2"><span className="font-medium">Observaciones:</span> {activo.observaciones ?? "-"}</div>
      </div>

      <h2 className="text-lg font-semibold mb-3">Historial de movimientos</h2>
      <HistorialTimeline movimientos={activo.movimientos} />

      <ReasignarModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        ubicaciones={ubicaciones}
        custodios={custodios}
        estados={estados}
        onReasignar={handleReasignar}
      />
    </div>
  );
}

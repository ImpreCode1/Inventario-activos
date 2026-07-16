"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";

import { api } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { ActivoFilters } from "@/components/activos/ActivoFilters";
import { ActivosTable, ActivoRow } from "@/components/activos/ActivosTable";
import { TableSkeleton } from "@/components/ui/LoadingSkeleton";
import { useToast } from "@/components/ui/Toast";

interface SelectOption {
  value: string;
  label: string;
}

interface Categoria { id: number; nombre: string }
interface Ubicacion { id: number; nombre: string }
interface EstadoActivo { id: number; nombre: string }
interface PaginatedResponse<T> { items: T[]; total: number }

export default function ActivosPage() {
  const [activos, setActivos] = useState<ActivoRow[]>([]);
  const [total, setTotal] = useState(0);
  const [categorias, setCategorias] = useState<SelectOption[]>([]);
  const [ubicaciones, setUbicaciones] = useState<SelectOption[]>([]);
  const [estados, setEstados] = useState<SelectOption[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [skip, setSkip] = useState(0);
  const [filters, setFilters] = useState<Record<string, string>>({});
  const limit = 10;
  const { addToast } = useToast();

  const loadCatalogs = useCallback(async () => {
    try {
      const [cats, ubi, est] = await Promise.all([
        api.get<Categoria[]>("/api/v1/categorias"),
        api.get<Ubicacion[]>("/api/v1/ubicaciones"),
        api.get<EstadoActivo[]>("/api/v1/estados_activo").catch(() => [
          { id: 1, nombre: "Disponible" },
          { id: 2, nombre: "Asignado" },
          { id: 3, nombre: "En mantenimiento" },
          { id: 4, nombre: "Dado de baja" },
        ]),
      ]);
      setCategorias(cats.map((c) => ({ value: String(c.id), label: c.nombre })));
      setUbicaciones(ubi.map((u) => ({ value: String(u.id), label: u.nombre })));
      setEstados(est.map((e) => ({ value: String(e.id), label: e.nombre })));
    } catch (err: any) {
      addToast(err.detail || "Error al cargar catálogos", "error");
    }
  }, [addToast]);

  const loadActivos = useCallback(async (currentSkip: number, currentFilters: Record<string, string>) => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams({ ...currentFilters, skip: String(currentSkip), limit: String(limit) });
      const data = await api.get<PaginatedResponse<ActivoRow>>(`/api/v1/activos?${params}`);
      setActivos(data.items);
      setTotal(data.total);
    } catch (err: any) {
      setError(err.detail || "Error al cargar activos");
      addToast(err.detail || "Error al cargar activos", "error");
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  useEffect(() => { loadCatalogs(); }, [loadCatalogs]);
  useEffect(() => { loadActivos(skip, filters); }, [skip, filters, loadActivos]);

  const handleFilter = (newFilters: Record<string, string>) => {
    setFilters(newFilters);
    setSkip(0);
  };

  const hasMore = skip + limit < total;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Activos</h1>
        <Link href="/activos/nuevo"><Button>Nuevo activo</Button></Link>
      </div>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <ActivoFilters categorias={categorias} ubicaciones={ubicaciones} estados={estados} onFilter={handleFilter} />
      {loading ? (
        <TableSkeleton rows={5} cols={6} />
      ) : (
        <ActivosTable
          data={activos}
          skip={skip}
          limit={limit}
          hasMore={hasMore}
          onPrev={() => setSkip((s) => Math.max(0, s - limit))}
          onNext={() => setSkip((s) => s + limit)}
        />
      )}
      <p className="text-sm text-gray-500 mt-2">
        Mostrando {activos.length} de {total} activos
      </p>
    </div>
  );
}

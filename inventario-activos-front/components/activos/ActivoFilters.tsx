"use client";

import { Select } from "@/components/ui/Select";
import { Button } from "@/components/ui/Button";
import { useState, useEffect } from "react";
import { useDebounce } from "@/hooks/useDebounce";

interface SelectOption {
  value: string;
  label: string;
}

interface ActivoFiltersProps {
  categorias: SelectOption[];
  ubicaciones: SelectOption[];
  estados: SelectOption[];
  onFilter: (filters: Record<string, string>) => void;
}

export function ActivoFilters({ categorias, ubicaciones, estados, onFilter }: ActivoFiltersProps) {
  const [search, setSearch] = useState("");
  const [categoriaId, setCategoriaId] = useState("");
  const [ubicacionId, setUbicacionId] = useState("");
  const [estadoId, setEstadoId] = useState("");

  const debouncedSearch = useDebounce(search, 300);

  const buildParams = () => {
    const params: Record<string, string> = {};
    if (debouncedSearch) params.search = debouncedSearch;
    if (categoriaId) params.categoria_id = categoriaId;
    if (ubicacionId) params.ubicacion_id = ubicacionId;
    if (estadoId) params.estado_id = estadoId;
    return params;
  };

  useEffect(() => {
    onFilter(buildParams());
  }, [debouncedSearch, categoriaId, ubicacionId, estadoId]);

  return (
    <div className="flex flex-wrap gap-4 items-end mb-4">
      <div>
        <label className="block text-sm font-medium text-gray-900 mb-1">Búsqueda</label>
        <input
          className="border rounded px-3 py-2 w-48"
          placeholder="Código, nombre, serial..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>
      <Select label="Categoría" options={categorias} value={categoriaId} onChange={(e) => setCategoriaId(e.target.value)} />
      <Select label="Ubicación" options={ubicaciones} value={ubicacionId} onChange={(e) => setUbicacionId(e.target.value)} />
      <Select label="Estado" options={estados} value={estadoId} onChange={(e) => setEstadoId(e.target.value)} />
      <Button onClick={() => onFilter(buildParams())}>Filtrar</Button>
    </div>
  );
}

"use client";

import { useEffect, useState, useCallback } from "react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { UbicacionTree, UbicacionArbol } from "@/components/ubicaciones/UbicacionTree";

export default function UbicacionesPage() {
  const [arbol, setArbol] = useState<UbicacionArbol[]>([]);
  const [error, setError] = useState("");
  const [creando, setCreando] = useState(false);
  const [nombre, setNombre] = useState("");
  const [nivel, setNivel] = useState("");

  const load = useCallback(() => {
    api.get<UbicacionArbol[]>("/api/v1/ubicaciones/arbol")
      .then(setArbol)
      .catch((err) => setError(err.detail || "Error al cargar"));
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleCreate = async () => {
    if (!nombre.trim()) return;
    try {
      await api.post("/api/v1/ubicaciones", { nombre, nivel: nivel || null, ubicacion_padre_id: null });
      setNombre("");
      setNivel("");
      setCreando(false);
      load();
    } catch (err: any) {
      setError(err.detail || "Error al crear");
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/api/v1/ubicaciones/${id}`);
      load();
    } catch (err: any) {
      throw err;
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Ubicaciones</h1>
        <Button onClick={() => setCreando(!creando)}>{creando ? "Cancelar" : "Nueva ubicación"}</Button>
      </div>
      {error && <p className="text-red-500 mb-2">{error}</p>}

      {creando && (
        <div className="bg-white p-4 rounded shadow mb-4 flex gap-4 items-end">
          <div>
            <label className="block text-sm font-medium text-gray-900">Nombre</label>
            <input className="border rounded px-3 py-2" value={nombre} onChange={(e) => setNombre(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-900">Nivel</label>
            <select className="border rounded px-3 py-2" value={nivel} onChange={(e) => setNivel(e.target.value)}>
              <option value="">--</option>
              <option value="sede">Sede</option>
              <option value="area">Área</option>
              <option value="espacio">Espacio</option>
            </select>
          </div>
          <Button onClick={handleCreate}>Crear</Button>
        </div>
      )}

      <div className="bg-white p-4 rounded shadow">
        <UbicacionTree nodos={arbol} onDelete={handleDelete} />
      </div>
    </div>
  );
}

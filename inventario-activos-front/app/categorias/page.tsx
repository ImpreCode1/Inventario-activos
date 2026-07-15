"use client";

import { useEffect, useState, useCallback } from "react";
import { api, ApiError } from "@/lib/api";
import { Table } from "@/components/ui/Table";
import { Button } from "@/components/ui/Button";
import { Modal } from "@/components/ui/Modal";
import { Badge } from "@/components/ui/Badge";

interface Categoria {
  id: number;
  nombre: string;
  descripcion?: string | null;
  activo: boolean;
}

export default function CategoriasPage() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [error, setError] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editando, setEditando] = useState<Categoria | null>(null);
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(() => {
    api.get<Categoria[]>("/api/v1/categorias")
      .then(setCategorias)
      .catch((err) => setError(err.detail || "Error al cargar"));
  }, []);

  useEffect(() => { load(); }, [load]);

  const openCreate = () => {
    setEditando(null);
    setNombre("");
    setDescripcion("");
    setModalOpen(true);
  };

  const openEdit = (cat: Categoria) => {
    setEditando(cat);
    setNombre(cat.nombre);
    setDescripcion(cat.descripcion ?? "");
    setModalOpen(true);
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      if (editando) {
        await api.put(`/api/v1/categorias/${editando.id}`, { nombre, descripcion });
      } else {
        await api.post("/api/v1/categorias", { nombre, descripcion });
      }
      setModalOpen(false);
      load();
    } catch (err: any) {
      setError(err.detail || "Error al guardar");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("¿Desactivar categoría?")) return;
    try {
      await api.delete(`/api/v1/categorias/${id}`);
      load();
    } catch (err: any) {
      setError(err.detail || "Error al desactivar");
    }
  };

  const columns = [
    { key: "id", header: "ID" },
    { key: "nombre", header: "Nombre" },
    { key: "descripcion", header: "Descripción", render: (r: Categoria) => r.descripcion ?? "-" },
    {
      key: "activo",
      header: "Estado",
      render: (r: Categoria) => <Badge text={r.activo ? "Activo" : "Inactivo"} variant={r.activo ? "success" : "danger"} />,
    },
    {
      key: "acciones",
      header: "",
      render: (r: Categoria) => (
        <div className="flex gap-2">
          <Button variant="secondary" type="button" onClick={() => openEdit(r)}>Editar</Button>
          {r.activo && <Button variant="danger" type="button" onClick={() => handleDelete(r.id)}>Desactivar</Button>}
        </div>
      ),
    },
  ];

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Categorías</h1>
        <Button onClick={openCreate}>Nueva categoría</Button>
      </div>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <Table columns={columns} data={categorias} keyExtractor={(r: Categoria) => r.id} />

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title={editando ? "Editar categoría" : "Nueva categoría"}>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-900">Nombre *</label>
            <input className="border rounded px-3 py-2 w-full" required value={nombre} onChange={(e) => setNombre(e.target.value)} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-900">Descripción</label>
            <textarea className="border rounded px-3 py-2 w-full" rows={3} value={descripcion} onChange={(e) => setDescripcion(e.target.value)} />
          </div>
          <div className="flex justify-end gap-2">
            <Button variant="secondary" onClick={() => setModalOpen(false)}>Cancelar</Button>
            <Button onClick={handleSubmit} loading={submitting}>{editando ? "Guardar" : "Crear"}</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}

"use client";

import { useState } from "react";
import { Button } from "@/components/ui/Button";
import { Select } from "@/components/ui/Select";

interface SelectOption {
  value: string;
  label: string;
}

interface ActivoFormData {
  codigo_interno: string;
  nombre: string;
  marca: string;
  modelo: string;
  serial: string;
  valor: string;
  categoria_id: string;
  ubicacion_id: string;
  custodio_id: string;
  estado_id: string;
  fecha_adquisicion: string;
  observaciones: string;
}

interface ActivoFormProps {
  initial?: Partial<ActivoFormData>;
  categorias: SelectOption[];
  ubicaciones: SelectOption[];
  estados: SelectOption[];
  custodios: SelectOption[];
  onSubmit: (data: ActivoFormData) => Promise<void>;
  mode: "create" | "edit";
}

export function ActivoForm({ initial, categorias, ubicaciones, estados, custodios, onSubmit, mode }: ActivoFormProps) {
  const [form, setForm] = useState<ActivoFormData>({
    codigo_interno: initial?.codigo_interno ?? "",
    nombre: initial?.nombre ?? "",
    marca: initial?.marca ?? "",
    modelo: initial?.modelo ?? "",
    serial: initial?.serial ?? "",
    valor: initial?.valor ?? "",
    categoria_id: initial?.categoria_id ?? "",
    ubicacion_id: initial?.ubicacion_id ?? "",
    custodio_id: initial?.custodio_id ?? "",
    estado_id: initial?.estado_id ?? "",
    fecha_adquisicion: initial?.fecha_adquisicion ?? "",
    observaciones: initial?.observaciones ?? "",
  });
  const [submitting, setSubmitting] = useState(false);

  const set = (field: keyof ActivoFormData) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit(form);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-xl">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-900">Código interno *</label>
          <input className="border rounded px-3 py-2 w-full" required value={form.codigo_interno} onChange={set("codigo_interno")} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-900">Nombre *</label>
          <input className="border rounded px-3 py-2 w-full" required value={form.nombre} onChange={set("nombre")} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-900">Marca</label>
          <input className="border rounded px-3 py-2 w-full" value={form.marca} onChange={set("marca")} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-900">Modelo</label>
          <input className="border rounded px-3 py-2 w-full" value={form.modelo} onChange={set("modelo")} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-900">Serial</label>
          <input className="border rounded px-3 py-2 w-full" value={form.serial} onChange={set("serial")} />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-900">Valor</label>
          <input className="border rounded px-3 py-2 w-full" type="number" step="0.01" value={form.valor} onChange={set("valor")} />
        </div>
        <Select label="Categoría *" options={categorias} value={form.categoria_id} onChange={set("categoria_id")} />
        <Select label="Ubicación" options={ubicaciones} value={form.ubicacion_id} onChange={set("ubicacion_id")} />
        <Select label="Custodio" options={custodios} value={form.custodio_id} onChange={set("custodio_id")} />
        <Select label="Estado *" options={estados} value={form.estado_id} onChange={set("estado_id")} />
        <div>
          <label className="block text-sm font-medium text-gray-900">Fecha adquisición</label>
          <input className="border rounded px-3 py-2 w-full" type="date" value={form.fecha_adquisicion} onChange={set("fecha_adquisicion")} />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-900">Observaciones</label>
        <textarea className="border rounded px-3 py-2 w-full" rows={3} value={form.observaciones} onChange={set("observaciones")} />
      </div>
      <Button type="submit" loading={submitting}>{mode === "create" ? "Crear" : "Guardar cambios"}</Button>
    </form>
  );
}

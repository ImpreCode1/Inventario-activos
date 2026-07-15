"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";

import { api } from "@/lib/api";
import { ActivoForm } from "@/components/activos/ActivoForm";

interface SelectOption {
  value: string;
  label: string;
}

export default function EditarActivoPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();

  const [categorias, setCategorias] = useState<SelectOption[]>([]);
  const [ubicaciones, setUbicaciones] = useState<SelectOption[]>([]);
  const [estados, setEstados] = useState<SelectOption[]>([]);
  const [custodios, setCustodios] = useState<SelectOption[]>([]);
  const [initial, setInitial] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get<any>(`/api/v1/activos/${id}`),
      api.get<any[]>("/api/v1/categorias"),
      api.get<any[]>("/api/v1/ubicaciones"),
      api.get<any[]>("/api/v1/estados_activo").catch(() => [
        { id: 1, nombre: "Disponible" }, { id: 2, nombre: "Asignado" },
        { id: 3, nombre: "En mantenimiento" }, { id: 4, nombre: "Dado de baja" },
      ]),
      api.get<any[]>("/api/v1/usuarios").catch(() => []),
    ])
      .then(([act, cats, ubis, ests, usrs]) => {
        setInitial({
          codigo_interno: act.codigo_interno,
          nombre: act.nombre,
          marca: act.marca ?? "",
          modelo: act.modelo ?? "",
          serial: act.serial ?? "",
          valor: act.valor?.toString() ?? "",
          categoria_id: String(act.categoria_id),
          ubicacion_id: act.ubicacion_id ? String(act.ubicacion_id) : "",
          custodio_id: act.custodio_id ? String(act.custodio_id) : "",
          estado_id: String(act.estado_id),
          fecha_adquisicion: act.fecha_adquisicion ?? "",
          observaciones: act.observaciones ?? "",
        });
        setCategorias(cats.map((c: any) => ({ value: String(c.id), label: c.nombre })));
        setUbicaciones(ubis.map((u: any) => ({ value: String(u.id), label: u.nombre })));
        setEstados(ests.map((e: any) => ({ value: String(e.id), label: e.nombre })));
        setCustodios(usrs.map((u: any) => ({ value: String(u.id), label: u.nombre })));
      })
      .catch((err: any) => setError(err.detail || "Error al cargar datos"));
  }, [id]);

  const handleSubmit = async (data: any) => {
    const body: Record<string, any> = {};
    if (data.codigo_interno) body.codigo_interno = data.codigo_interno;
    if (data.nombre) body.nombre = data.nombre;
    body.marca = data.marca || null;
    body.modelo = data.modelo || null;
    body.serial = data.serial || null;
    body.valor = data.valor ? Number(data.valor) : null;
    if (data.categoria_id) body.categoria_id = Number(data.categoria_id);
    body.ubicacion_id = data.ubicacion_id ? Number(data.ubicacion_id) : null;
    body.custodio_id = data.custodio_id ? Number(data.custodio_id) : null;
    if (data.estado_id) body.estado_id = Number(data.estado_id);
    body.fecha_adquisicion = data.fecha_adquisicion || null;
    body.observaciones = data.observaciones || null;
    await api.put(`/api/v1/activos/${id}`, body);
    router.push(`/activos/${id}`);
  };

  if (error) return <p className="text-red-500">{error}</p>;
  if (!initial) return <p>Cargando...</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Editar activo</h1>
      <ActivoForm initial={initial} categorias={categorias} ubicaciones={ubicaciones} estados={estados} custodios={custodios} onSubmit={handleSubmit} mode="edit" />
    </div>
  );
}

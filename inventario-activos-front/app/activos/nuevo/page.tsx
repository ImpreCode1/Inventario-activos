"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { api } from "@/lib/api";
import { ActivoForm } from "@/components/activos/ActivoForm";

interface SelectOption {
  value: string;
  label: string;
}

export default function NuevoActivoPage() {
  const router = useRouter();
  const [categorias, setCategorias] = useState<SelectOption[]>([]);
  const [ubicaciones, setUbicaciones] = useState<SelectOption[]>([]);
  const [estados, setEstados] = useState<SelectOption[]>([]);
  const [custodios, setCustodios] = useState<SelectOption[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get<any[]>("/api/v1/categorias"),
      api.get<any[]>("/api/v1/ubicaciones"),
      api.get<any[]>("/api/v1/estados_activo").catch(() => [
        { id: 1, nombre: "Disponible" }, { id: 2, nombre: "Asignado" },
        { id: 3, nombre: "En mantenimiento" }, { id: 4, nombre: "Dado de baja" },
      ]),
      api.get<any[]>("/api/v1/usuarios").catch(() => []),
    ])
      .then(([cats, ubis, ests, usrs]) => {
        setCategorias(cats.map((c: any) => ({ value: String(c.id), label: c.nombre })));
        setUbicaciones(ubis.map((u: any) => ({ value: String(u.id), label: u.nombre })));
        setEstados(ests.map((e: any) => ({ value: String(e.id), label: e.nombre })));
        setCustodios(usrs.map((u: any) => ({ value: String(u.id), label: u.nombre })));
      })
      .catch((err: any) => setError(err.detail || "Error al cargar catálogos"));
  }, []);

  const handleSubmit = async (data: any) => {
    const body = {
      codigo_interno: data.codigo_interno,
      nombre: data.nombre,
      marca: data.marca || null,
      modelo: data.modelo || null,
      serial: data.serial || null,
      valor: data.valor ? Number(data.valor) : null,
      categoria_id: Number(data.categoria_id),
      ubicacion_id: data.ubicacion_id ? Number(data.ubicacion_id) : null,
      custodio_id: data.custodio_id ? Number(data.custodio_id) : null,
      estado_id: Number(data.estado_id),
      fecha_adquisicion: data.fecha_adquisicion || null,
      observaciones: data.observaciones || null,
    };
    await api.post("/api/v1/activos", body);
    router.push("/activos");
  };

  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Nuevo activo</h1>
      <ActivoForm categorias={categorias} ubicaciones={ubicaciones} estados={estados} custodios={custodios} onSubmit={handleSubmit} mode="create" />
    </div>
  );
}

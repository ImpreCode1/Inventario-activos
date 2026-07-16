"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { CardSkeleton } from "@/components/ui/LoadingSkeleton";
import { useToast } from "@/components/ui/Toast";

interface ConteoEstado {
  estado_id: number;
  estado_nombre: string;
  total: number;
}

interface ConteoCategoria {
  categoria_id: number;
  categoria_nombre: string;
  total: number;
}

interface DashboardData {
  por_estado: ConteoEstado[];
  por_categoria: ConteoCategoria[];
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState("");
  const { addToast } = useToast();

  useEffect(() => {
    api.get<DashboardData>("/api/v1/dashboard/resumen")
      .then(setData)
      .catch((err) => {
        const msg = err.detail || "Error al cargar dashboard";
        setError(msg);
        addToast(msg, "error");
      });
  }, [addToast]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!data) return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section>
          <h2 className="text-lg font-semibold mb-3 text-gray-900">Por Estado</h2>
          <div className="space-y-2">
            {[1, 2, 3].map((i) => <CardSkeleton key={i} />)}
          </div>
        </section>
        <section>
          <h2 className="text-lg font-semibold mb-3 text-gray-900">Por Categoría</h2>
          <div className="space-y-2">
            {[1, 2, 3].map((i) => <CardSkeleton key={i} />)}
          </div>
        </section>
      </div>
    </div>
  );

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <section>
          <h2 className="text-lg font-semibold mb-3 text-gray-900">Por Estado</h2>
          <div className="space-y-2">
            {data.por_estado.map((e) => (
              <div key={e.estado_id} className="flex justify-between bg-white p-3 rounded shadow">
                <span className="text-gray-900">{e.estado_nombre}</span>
                <span className="font-bold text-gray-900">{e.total}</span>
              </div>
            ))}
          </div>
        </section>
        <section>
          <h2 className="text-lg font-semibold mb-3 text-gray-900">Por Categoría</h2>
          <div className="space-y-2">
            {data.por_categoria.map((c) => (
              <div key={c.categoria_id} className="flex justify-between bg-white p-3 rounded shadow">
                <span className="text-gray-900">{c.categoria_nombre}</span>
                <span className="font-bold text-gray-900">{c.total}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

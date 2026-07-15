"use client";

import { useState } from "react";

import { Modal } from "@/components/ui/Modal";
import { Select } from "@/components/ui/Select";
import { Button } from "@/components/ui/Button";

interface SelectOption {
  value: string;
  label: string;
}

interface ReasignarModalProps {
  isOpen: boolean;
  onClose: () => void;
  ubicaciones: SelectOption[];
  custodios: SelectOption[];
  estados: SelectOption[];
  onReasignar: (body: Record<string, unknown>) => Promise<void>;
}

export function ReasignarModal({ isOpen, onClose, ubicaciones, custodios, estados, onReasignar }: ReasignarModalProps) {
  const [ubicacionId, setUbicacionId] = useState("");
  const [custodioId, setCustodioId] = useState("");
  const [estadoId, setEstadoId] = useState("");
  const [motivo, setMotivo] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const body: Record<string, unknown> = { motivo: motivo || null };
      body.ubicacion_id = ubicacionId ? Number(ubicacionId) : null;
      body.custodio_id = custodioId ? Number(custodioId) : null;
      body.estado_id = estadoId ? Number(estadoId) : null;
      await onReasignar(body);
      onClose();
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Reasignar activo">
      <div className="space-y-4">
        <Select label="Nueva ubicación" options={ubicaciones} value={ubicacionId} onChange={(e) => setUbicacionId(e.target.value)} />
        <Select label="Nuevo custodio" options={custodios} value={custodioId} onChange={(e) => setCustodioId(e.target.value)} />
        <Select label="Nuevo estado" options={estados} value={estadoId} onChange={(e) => setEstadoId(e.target.value)} />
        <div>
          <label className="block text-sm font-medium">Motivo</label>
          <textarea className="border rounded px-3 py-2 w-full" rows={3} value={motivo} onChange={(e) => setMotivo(e.target.value)} />
        </div>
        <div className="flex justify-end gap-2">
          <Button variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button onClick={handleSubmit} loading={submitting}>Reasignar</Button>
        </div>
      </div>
    </Modal>
  );
}

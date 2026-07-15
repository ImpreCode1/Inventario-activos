import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Inventario de Activos - Impresistem S.A.S.",
  description: "Sistema de Gestión de Inventario de Activos",
};

const navLinks = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/activos", label: "Activos" },
  { href: "/ubicaciones", label: "Ubicaciones" },
  { href: "/categorias", label: "Categorías" },
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es">
      <body>
        <div className="flex h-screen">
          <nav className="w-56 bg-gray-900 text-white p-4 flex flex-col gap-3">
            <h1 className="text-lg font-bold mb-4">Activos</h1>
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href} className="hover:text-blue-300 transition">
                {link.label}
              </Link>
            ))}
          </nav>
          <main className="flex-1 overflow-auto p-6 bg-gray-50">{children}</main>
        </div>
      </body>
    </html>
  );
}

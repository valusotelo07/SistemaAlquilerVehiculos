import customtkinter as ctk
from modelos.auto import Auto

class PanelDisponibilidad(ctk.CTkFrame):
    def __init__(self, master, sistema):
        super().__init__(master, fg_color="transparent")
        self.sistema = sistema

        ctk.CTkLabel(self, text="Vehiculos Disponibles", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(30, 5))
        ctk.CTkLabel(self, text="Vehiculos activos y sin alquiler vigente", font=("Arial", 13), text_color="gray").pack(pady=(0, 15))

        self.btn_actualizar = ctk.CTkButton(
            self, text="Actualizar", fg_color="#1f6aa5", hover_color="#144870",
            width=160, height=38, command=self.actualizar_lista
        )
        self.btn_actualizar.pack(pady=(0, 15))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=40, pady=(0, 30))

        self.actualizar_lista()

    def actualizar_lista(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        disponibles = self.sistema.verificar_disponibilidad()

        if not disponibles:
            ctk.CTkLabel(self.scroll, text="No hay vehiculos disponibles en este momento.", text_color="gray").pack(pady=30)
            return

        for v in disponibles:
            fila = ctk.CTkFrame(self.scroll, fg_color=("gray85", "gray20"), corner_radius=10)
            fila.pack(fill="x", pady=6)

            tipo = "Auto" if isinstance(v, Auto) else "Moto"
            retiro = v.get_sucursal_retiro() if v.get_sucursal_retiro() else "Sin definir"
            precio_fmt = f"{v.get_precio_por_dia():,.0f}".replace(",", ".")

            ctk.CTkLabel(fila, text=f"[{tipo}]  {v.get_marca()} {v.get_modelo()} — {v.get_patente()}",
                         font=("Arial", 14, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
            ctk.CTkLabel(fila, text=f"${precio_fmt}/dia  |  Retiro: {retiro}",
                         font=("Arial", 12), text_color="gray").pack(anchor="w", padx=15, pady=(0, 10))

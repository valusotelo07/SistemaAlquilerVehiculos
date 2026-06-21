import customtkinter as ctk
from modelos.sucursal import Sucursal
from gui.ventana_clientes import PanelClientes
from gui.ventana_alquileres import PanelAlquileres
from gui.ventana_vehiculos import PanelVehiculos

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, sucursal):
        super().__init__()
        self.sucursal = sucursal
        self.sistema = sucursal.get_sistema()

        self.title(f"NovaDrive - Sucursal {sucursal.get_nombre()}")
        self.geometry("900x600")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ==========================================
        # PANEL LATERAL (SIDEBAR)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="🚘 NovaDrive", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(30, 5))

        self.lbl_sucursal = ctk.CTkLabel(self.sidebar, text=f"📍 {sucursal.get_nombre()}\n{sucursal.get_direccion()}", font=("Arial", 11), text_color="gray", justify="center")
        self.lbl_sucursal.grid(row=1, column=0, padx=20, pady=(0, 15))

        # Botones del Menú Lateral
        self.btn_menu_clientes = ctk.CTkButton(self.sidebar, text="👥 Clientes", fg_color="transparent", text_color="white", hover_color="gray30", anchor="w", font=("Arial", 15), command=self.mostrar_panel_clientes)
        self.btn_menu_clientes.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_menu_vehiculos = ctk.CTkButton(self.sidebar, text="🚙 Vehículos", fg_color="transparent", text_color="white", hover_color="gray30", anchor="w", font=("Arial", 15), command=self.mostrar_panel_vehiculos)
        self.btn_menu_vehiculos.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.btn_menu_alquileres = ctk.CTkButton(self.sidebar, text="📄 Alquileres", fg_color="transparent", text_color="white", hover_color="gray30", anchor="w", font=("Arial", 15), command=self.mostrar_panel_alquileres)
        self.btn_menu_alquileres.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # ==========================================
        # PANEL CENTRAL (VISTA PRINCIPAL)
        # ==========================================
        self.panel_central = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.panel_central.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.lbl_bienvenida = ctk.CTkLabel(self.panel_central, text="Bienvenido a NovaDrive", font=ctk.CTkFont(size=28, weight="bold"))
        self.lbl_bienvenida.pack(pady=(150, 10))

        self.lbl_subtitulo = ctk.CTkLabel(self.panel_central, text="Seleccioná una opción del menú lateral para comenzar.", font=("Arial", 16), text_color="gray")
        self.lbl_subtitulo.pack()

    def _mostrar_panel(self, cls, *args):
        for widget in self.panel_central.winfo_children():
            widget.destroy()
        cls(self.panel_central, self.sistema, *args).pack(fill="both", expand=True)

    def mostrar_panel_clientes(self):
        self._mostrar_panel(PanelClientes)

    def mostrar_panel_vehiculos(self):
        self._mostrar_panel(PanelVehiculos)

    def mostrar_panel_alquileres(self):
        self._mostrar_panel(PanelAlquileres, self.sucursal)

# --- EJECUCIÓN DE LA APP ---
if __name__ == "__main__":
    sucursal = Sucursal(1, "Central", "Av. Corrientes 1234")
    app = App(sucursal)
    app.mainloop()

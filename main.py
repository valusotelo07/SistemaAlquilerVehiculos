import customtkinter as ctk
from modelos.sucursal import Sucursal
from gui.ventana_clientes import PanelClientes
from gui.ventana_alquileres import PanelAlquileres
from gui.ventana_vehiculos import PanelVehiculos
from sistema.sistema_alquiler import SistemaAlquiler
from gui.panel_inicio import PanelInicio
import os
import shutil 


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, sucursal):
        super().__init__()
        self.sucursal = sucursal
        self.sistema = SistemaAlquiler()

        self.title(f"NovaDrive - Sucursal {sucursal.get_nombre()}")
        self.geometry("900x600")
        self.protocol("WM_DELETE_WINDOW", self.cerrar_programa)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

       # ==========================================
        # PANEL LATERAL (SIDEBAR)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1) # Subimos a 6 para empujar el resto hacia abajo

        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="🚘 NovaDrive", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(30, 5))

        self.lbl_sucursal = ctk.CTkLabel(self.sidebar, text=f"📍 {sucursal.get_nombre()}\n{sucursal.get_direccion()}", font=("Arial", 11), text_color="gray", justify="center")
        self.lbl_sucursal.grid(row=1, column=0, padx=20, pady=(0, 15))

       # Botón INICIO
        self.btn_menu_inicio = ctk.CTkButton(self.sidebar, text="🏠 Inicio", fg_color="transparent", text_color=("black", "white"), hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15), command=self.mostrar_panel_inicio)
        self.btn_menu_inicio.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Botón CLIENTES
        self.btn_menu_clientes = ctk.CTkButton(self.sidebar, text="👥 Clientes", fg_color="transparent", text_color=("black", "white"), hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15), command=self.mostrar_panel_clientes)
        self.btn_menu_clientes.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Botón VEHÍCULOS
        self.btn_menu_vehiculos = ctk.CTkButton(self.sidebar, text="🚙 Vehículos", fg_color="transparent", text_color=("black", "white"), hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15), command=self.mostrar_panel_vehiculos)
        self.btn_menu_vehiculos.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        # Botón ALQUILERES
        self.btn_menu_alquileres = ctk.CTkButton(self.sidebar, text="📄 Alquileres", fg_color="transparent", text_color=("black", "white"), hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15), command=self.mostrar_panel_alquileres)
        self.btn_menu_alquileres.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        # ==========================================
        # SWITCH DE MODO CLARO / OSCURO
        # ==========================================
        self.sidebar.grid_rowconfigure(6, weight=1) 
        
        self.switch_modo = ctk.CTkSwitch(self.sidebar, text="Modo Oscuro", command=self.cambiar_modo)
       
        self.switch_modo.grid(row=7, column=0, padx=20, pady=(10, 20), sticky="s")
        
        self.switch_modo.select()

        # ==========================================
        # PANEL CENTRAL (VISTA PRINCIPAL)
        # ==========================================
        self.panel_central = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.panel_central.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        
        self.mostrar_panel_inicio()

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

    def mostrar_panel_inicio(self):
        for widget in self.panel_central.winfo_children():
            widget.destroy()
            
        vista = PanelInicio(self.panel_central, self.sistema)
        vista.pack(fill="both", expand=True)

    def cerrar_programa(self):
        ruta_tickets = os.path.join(os.path.dirname(__file__), "tickets")
        
        
        if os.path.exists(ruta_tickets):
            try:
                shutil.rmtree(ruta_tickets)
                print("Limpieza: Carpeta de tickets eliminada con éxito.")
            except Exception as e:
                print(f"Aviso: No se pudo limpiar la carpeta de tickets - {e}")
        self.destroy()

    def cambiar_modo(self):
        if self.switch_modo.get() == 1:
            ctk.set_appearance_mode("dark")
            self.switch_modo.configure(text="Modo Oscuro")
        else:
            ctk.set_appearance_mode("light")
            self.switch_modo.configure(text="Modo Claro")

# --- EJECUCIÓN DE LA APP ---
if __name__ == "__main__":
    sucursal = Sucursal(1, "Central", "Av. Corrientes 1234")
    app = App(sucursal)
    app.mainloop()

import customtkinter as ctk
from sistema.sistema_alquiler import SistemaAlquiler
from gui.ventana_clientes import PanelClientes
from gui.ventana_alquileres import PanelAlquileres
from gui.ventana_vehiculos import PanelVehiculos

# Instanciamos el sistema central
sistema = SistemaAlquiler()

# Configuración visual Premium
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURACIÓN DE LA VENTANA PRINCIPAL ---
        self.title("NovaDrive - Sistema de Gestión")
        self.geometry("900x600")
        
        # Dividimos la pantalla: Columna 0 (Sidebar, no se expande) y Columna 1 (Centro, se expande)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # ==========================================
        # PANEL LATERAL (SIDEBAR)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1) # Empuja el último botón hacia abajo

        # Logo / Título del Sidebar
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="🚘 NovaDrive", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(30, 20))

        # Botones del Menú Lateral (con estilo transparente que se ilumina al pasar el mouse)
        self.btn_menu_clientes = ctk.CTkButton(self.sidebar, text="👥 Clientes", fg_color="transparent", text_color="white", hover_color="gray30", anchor="w", font=("Arial", 15), command=self.mostrar_panel_clientes)
        self.btn_menu_clientes.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        
        self.btn_menu_vehiculos = ctk.CTkButton(self.sidebar, text="🚙 Vehículos", fg_color="transparent", text_color="white", hover_color="gray30", anchor="w", font=("Arial", 15), command=self.mostrar_panel_vehiculos)
        self.btn_menu_vehiculos.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.btn_menu_alquileres = ctk.CTkButton(self.sidebar, text="📄 Alquileres", fg_color="transparent", text_color="white", hover_color="gray30", anchor="w", font=("Arial", 15), command=self.mostrar_panel_alquileres)
        self.btn_menu_alquileres.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # ==========================================
        # PANEL CENTRAL (VISTA PRINCIPAL)
        # ==========================================
        self.panel_central = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.panel_central.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Pantalla de Bienvenida por defecto
        self.lbl_bienvenida = ctk.CTkLabel(self.panel_central, text="Bienvenido a NovaDrive", font=ctk.CTkFont(size=28, weight="bold"))
        self.lbl_bienvenida.pack(pady=(150, 10))
        
        self.lbl_subtitulo = ctk.CTkLabel(self.panel_central, text="Seleccioná una opción del menú lateral para comenzar.", font=("Arial", 16), text_color="gray")
        self.lbl_subtitulo.pack()

    def mostrar_panel_clientes(self):
        # 1. Borramos todo lo que haya en el panel central (ej: el mensaje de bienvenida)
        for widget in self.panel_central.winfo_children():
            widget.destroy()
            
        # 2. Instanciamos el nuevo panel pasándole el central como dueño
        vista = PanelClientes(self.panel_central, sistema)
        
        # 3. Lo empaquetamos para que ocupe todo el espacio
        vista.pack(fill="both", expand=True)

    def mostrar_panel_vehiculos(self):
        for widget in self.panel_central.winfo_children():
            widget.destroy()
            
        vista = PanelVehiculos(self.panel_central, sistema)
        vista.pack(fill="both", expand=True)

    def mostrar_panel_alquileres(self):
        for widget in self.panel_central.winfo_children():
            widget.destroy()
            
        vista = PanelAlquileres(self.panel_central, sistema)
        vista.pack(fill="both", expand=True)

# --- EJECUCIÓN DE LA APP ---
if __name__ == "__main__":
    app = App()
    app.mainloop()
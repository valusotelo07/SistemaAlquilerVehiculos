import customtkinter as ctk
from modelos.sucursal import Sucursal
from modelos.empleado import Empleado
from modelos.auto import Auto
from modelos.moto import Moto
from modelos.cliente import Cliente
from sistema.sistema_alquiler import SistemaAlquiler
from gui.ventana_login import VentanaLogin
from gui.ventana_clientes import PanelClientes
from gui.ventana_alquileres import PanelAlquileres
from gui.ventana_vehiculos import PanelVehiculos
from gui.ventana_disponibilidad import PanelDisponibilidad
from gui.ventana_admin import PanelAdmin
from gui.panel_inicio import PanelInicio
import os
import shutil

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, sucursal, sistema, empleado_activo):
        super().__init__()
        self.sucursal = sucursal
        self.sistema = sistema
        self.empleado_activo = empleado_activo
        self.volver_al_login = False

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
        self.sidebar.grid_rowconfigure(9, weight=1)

        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="NovaDrive", font=ctk.CTkFont(size=24, weight="bold"))
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(25, 3))

        self.lbl_sucursal = ctk.CTkLabel(
            self.sidebar, text=f"{sucursal.get_nombre()}\n{sucursal.get_direccion()}",
            font=("Arial", 11), text_color="gray", justify="center"
        )
        self.lbl_sucursal.grid(row=1, column=0, padx=20, pady=(0, 3))

        emp_nombre = f"{empleado_activo.get_nombre()} {empleado_activo.get_apellido()}"
        emp_rol = empleado_activo.get_rol().upper()
        self.lbl_empleado = ctk.CTkLabel(
            self.sidebar, text=f"{emp_nombre}\n[{emp_rol}]",
            font=("Arial", 11), text_color="#e5a50a" if emp_rol == "ADMIN" else "gray", justify="center"
        )
        self.lbl_empleado.grid(row=2, column=0, padx=20, pady=(0, 12))

        self.btn_menu_inicio = ctk.CTkButton(
            self.sidebar, text="Inicio", fg_color="transparent", text_color=("black", "white"),
            hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15),
            command=self.mostrar_panel_inicio
        )
        self.btn_menu_inicio.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.btn_menu_clientes = ctk.CTkButton(
            self.sidebar, text="Clientes", fg_color="transparent", text_color=("black", "white"),
            hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15),
            command=self.mostrar_panel_clientes
        )
        self.btn_menu_clientes.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

        self.btn_menu_vehiculos = ctk.CTkButton(
            self.sidebar, text="Vehiculos", fg_color="transparent", text_color=("black", "white"),
            hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15),
            command=self.mostrar_panel_vehiculos
        )
        self.btn_menu_vehiculos.grid(row=5, column=0, padx=20, pady=5, sticky="ew")

        self.btn_menu_alquileres = ctk.CTkButton(
            self.sidebar, text="Alquileres", fg_color="transparent", text_color=("black", "white"),
            hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15),
            command=self.mostrar_panel_alquileres
        )
        self.btn_menu_alquileres.grid(row=6, column=0, padx=20, pady=5, sticky="ew")

        self.btn_menu_disponibilidad = ctk.CTkButton(
            self.sidebar, text="Disponibilidad", fg_color="transparent", text_color=("black", "white"),
            hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 15),
            command=self.mostrar_panel_disponibilidad
        )
        self.btn_menu_disponibilidad.grid(row=7, column=0, padx=20, pady=5, sticky="ew")

        if empleado_activo.get_rol() == "admin":
            self.btn_menu_admin = ctk.CTkButton(
                self.sidebar, text="Administracion", fg_color="#1f6aa5", text_color="white",
                hover_color="#144870", cursor="hand2", anchor="w", font=("Arial", 15),
                command=self.mostrar_panel_admin
            )
            self.btn_menu_admin.grid(row=8, column=0, padx=20, pady=5, sticky="ew")

        self.btn_logout = ctk.CTkButton(
            self.sidebar, text="Cerrar Sesion", fg_color="transparent", text_color=("black", "gray"),
            hover_color=("gray70", "gray30"), cursor="hand2", anchor="w", font=("Arial", 13),
            command=self.cerrar_sesion
        )
        self.btn_logout.grid(row=9, column=0, padx=20, pady=(0, 5), sticky="ew")

        self.switch_modo = ctk.CTkSwitch(self.sidebar, text="Modo Oscuro", command=self.cambiar_modo)
        self.switch_modo.grid(row=10, column=0, padx=20, pady=(5, 20), sticky="s")
        self.switch_modo.select()

        # ==========================================
        # PANEL CENTRAL
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
        self._mostrar_panel(PanelAlquileres, self.sucursal, self.empleado_activo)

    def mostrar_panel_disponibilidad(self):
        self._mostrar_panel(PanelDisponibilidad)

    def mostrar_panel_admin(self):
        self._mostrar_panel(PanelAdmin)

    def mostrar_panel_inicio(self):
        for widget in self.panel_central.winfo_children():
            widget.destroy()
        PanelInicio(self.panel_central, self.sistema).pack(fill="both", expand=True)

    def cerrar_sesion(self):
        self.volver_al_login = True
        self.destroy()

    def cerrar_programa(self):
        ruta_tickets = os.path.join(os.path.dirname(__file__), "tickets")
        if os.path.exists(ruta_tickets):
            try:
                shutil.rmtree(ruta_tickets)
                print("Limpieza: Carpeta de tickets eliminada con exito.")
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


# --- EJECUCION DE LA APP ---
if __name__ == "__main__":
    sistema = SistemaAlquiler()
    sucursal = Sucursal(1, "Central", "Av. Corrientes 1234")

    # Empleados
    sistema.registrar_empleado(Empleado(1, "Admin",     "Sistema",     "admin",     "admin123", "admin"))
    sistema.registrar_empleado(Empleado(2, "Octavio",   "Valenzuela",  "octavio",   "oct123",   "empleado"))
    sistema.registrar_empleado(Empleado(3, "Franco",    "Duhalde",     "franco",    "fra123",   "empleado"))
    sistema.registrar_empleado(Empleado(4, "Antonella", "Da Silveira", "antonella", "ant123",   "empleado"))

    # Vehiculos de muestra
    sistema.registrar_vehiculo(Auto(1,  "AB123CD", "Toyota",     "Corolla",  28000, 4, "Sucursal Central"))
    sistema.registrar_vehiculo(Auto(2,  "BC456DE", "Volkswagen", "Gol",      18000, 4, "Sucursal Central"))
    sistema.registrar_vehiculo(Auto(3,  "CD789EF", "Ford",       "Focus",    24000, 4, "Sucursal Norte"))
    sistema.registrar_vehiculo(Auto(4,  "DE012FG", "Chevrolet",  "Cruze",    30000, 4, "Sucursal Norte"))
    sistema.registrar_vehiculo(Auto(5,  "EF345GH", "Renault",    "Sandero",  16000, 4, "Sucursal Sur"))
    sistema.registrar_vehiculo(Auto(6,  "FG678HI", "Peugeot",    "208",      22000, 4, "Sucursal Sur"))
    sistema.registrar_vehiculo(Moto(7,  "GH901IJ", "Honda",      "CB500",    12000, 500, "Sucursal Central"))
    sistema.registrar_vehiculo(Moto(8,  "HI234JK", "Yamaha",     "FZ25",     10000, 250, "Sucursal Norte"))
    sistema.registrar_vehiculo(Moto(9,  "IJ567KL", "Kawasaki",   "Ninja 400",14000, 400, "Sucursal Sur"))
    sistema.registrar_vehiculo(Moto(10, "JK890LM", "Bajaj",      "Pulsar NS200", 9000, 200, "Sucursal Central"))

    # Clientes de muestra
    sistema.registrar_cliente(Cliente(1, "30123456", "Martin",  "Gomez"))
    sistema.registrar_cliente(Cliente(2, "27654321", "Sofia",   "Lopez"))
    sistema.registrar_cliente(Cliente(3, "35987654", "Nicolas", "Rodriguez"))

    while True:
        login = VentanaLogin(sistema)
        login.mainloop()

        if login.empleado_autenticado is None:
            break

        app = App(sucursal, sistema, login.empleado_autenticado)
        app.mainloop()

        if not app.volver_al_login:
            break

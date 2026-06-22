import customtkinter as ctk
import os
from PIL import Image

class PanelInicio(ctk.CTkFrame):
    def __init__(self, master, sistema):
        super().__init__(master, fg_color="transparent")
        self.sistema = sistema

        self.lbl_titulo = ctk.CTkLabel(self, text="Panel de Control", font=ctk.CTkFont(size=28, weight="bold"))
        self.lbl_titulo.pack(pady=(40, 30))

        self.frame_tarjetas = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tarjetas.pack(pady=10, padx=20, fill="x")

        base_dir = os.path.dirname(os.path.dirname(__file__))
        ruta_assets = os.path.join(base_dir, "assets")

        try:
            icono_clientes = ctk.CTkImage(Image.open(os.path.join(ruta_assets, "clientes.png")), size=(45, 45))
            icono_vehiculos = ctk.CTkImage(Image.open(os.path.join(ruta_assets, "vehiculos.png")), size=(45, 45))
            icono_alquileres = ctk.CTkImage(Image.open(os.path.join(ruta_assets, "alquileres.png")), size=(45, 45))
        except Exception as e:
            print(f"Aviso: No se encontraron las imagenes. Error: {e}")
            icono_clientes = icono_vehiculos = icono_alquileres = None

        total_clientes = len(self.sistema.obtener_clientes())
        total_vehiculos = len(self.sistema.obtener_vehiculos())
        total_alquileres = len(self.sistema.obtener_alquileres())

        self.crear_tarjeta(self.frame_tarjetas, "Clientes", total_clientes, "#1f6aa5", 0, icono_clientes)
        self.crear_tarjeta(self.frame_tarjetas, "Vehiculos", total_vehiculos, "#2FA572", 1, icono_vehiculos)
        self.crear_tarjeta(self.frame_tarjetas, "Alquileres", total_alquileres, "#e5a50a", 2, icono_alquileres)

    def crear_tarjeta(self, master, titulo, valor, color_borde, columna, icono):
        tarjeta = ctk.CTkFrame(master, corner_radius=10, border_width=2, border_color=color_borde)
        tarjeta.grid(row=0, column=columna, padx=15, pady=10, sticky="ew")

        master.grid_columnconfigure(columna, weight=1)

        if icono:
            lbl_icono = ctk.CTkLabel(tarjeta, text="", image=icono)
            lbl_icono.pack(pady=(15, 0))

        lbl_titulo = ctk.CTkLabel(tarjeta, text=titulo, font=("Arial", 16, "bold"))
        margen_superior = 5 if icono else 15
        lbl_titulo.pack(pady=(margen_superior, 5))

        lbl_valor = ctk.CTkLabel(tarjeta, text=str(valor), font=ctk.CTkFont(size=36, weight="bold"), text_color=color_borde)
        lbl_valor.pack(pady=(0, 15))

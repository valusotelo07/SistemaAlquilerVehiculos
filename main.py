import customtkinter as ctk
from sistema.sistema_alquiler import SistemaAlquiler
from gui.ventana_clientes import VentanaClientes
from gui.ventana_vehiculos import VentanaVehiculos
from gui.ventana_alquileres import VentanaAlquileres

# Instanciamos el sistema central (el cerebro de la app)
sistema = SistemaAlquiler()

# Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Alquiler de Vehículos")
app.geometry("800x500")

# Título principal
titulo = ctk.CTkLabel(app, text="Sistema de Alquiler de Vehículos", font=("Arial", 24, "bold"))
titulo.pack(pady=30)

# --- FUNCIONES PARA ABRIR LA VENTANAS---
def abrir_ventana_clientes():
    VentanaClientes(app, sistema)


def abrir_ventana_vehiculos():
    VentanaVehiculos(app, sistema)


def abrir_ventana_alquileres():
    VentanaAlquileres(app, sistema)

    

# --- BOTONES DEL MENÚ ---
btn_cliente = ctk.CTkButton(app, text="Registrar Cliente", command=abrir_ventana_clientes, width=200, height=40)
btn_cliente.pack(pady=10)

btn_vehiculo = ctk.CTkButton(app, text="Registrar Vehículo", command=abrir_ventana_vehiculos, width=200, height=40)
btn_vehiculo.pack(pady=10)

btn_alquiler = ctk.CTkButton(app, text="Generar Alquiler", command=abrir_ventana_alquileres, width=200, height=40)
btn_alquiler.pack(pady=10)

app.mainloop()
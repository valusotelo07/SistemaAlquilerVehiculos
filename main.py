import customtkinter as ctk

# Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear ventana principal
app = ctk.CTk()

app.title("Sistema de Alquiler de Vehículos")
app.geometry("800x500")

# Título
titulo = ctk.CTkLabel(
    app,
    text="Sistema de Alquiler de Vehículos",
    font=("Arial", 24, "bold")
)
titulo.pack(pady=20)

# Botones de prueba
btn_cliente = ctk.CTkButton(app, text="Registrar Cliente")
btn_cliente.pack(pady=10)

btn_vehiculo = ctk.CTkButton(app, text="Registrar Vehículo")
btn_vehiculo.pack(pady=10)

btn_alquiler = ctk.CTkButton(app, text="Generar Alquiler")
btn_alquiler.pack(pady=10)

from modelos.auto import Auto
from modelos.moto import Moto

auto = Auto(1, "ABC123", "Toyota", "Corolla", 10000, 4)
moto = Moto(2, "XYZ456", "Honda", "CB500", 8000, 500)

print(auto.calcular_tarifa(3))
print(moto.calcular_tarifa(3))

app.mainloop()
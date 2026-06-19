import customtkinter as ctk
from tkinter import messagebox
from modelos.auto import Auto
from modelos.moto import Moto

class VentanaVehiculos(ctk.CTkToplevel):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema 
        
        self.title("Registrar Nuevo Vehículo")
        self.geometry("450x550") # Un poco más alta porque tiene más campos
        
        # Para que quede por encima de la principal
        self.transient(master)
        self.grab_set()

        self.lbl_titulo = ctk.CTkLabel(self, text="Datos del Vehículo", font=("Arial", 18, "bold"))
        self.lbl_titulo.pack(pady=(15, 10))
        
        # --- SELECTOR DE TIPO (AUTO O MOTO) ---
        self.tipo_var = ctk.StringVar(value="Auto")
        self.opcion_tipo = ctk.CTkOptionMenu(
            self, 
            values=["Auto", "Moto"], 
            variable=self.tipo_var,
            command=self.cambiar_tipo # Llama a esta función cuando elegís una opción
        )
        self.opcion_tipo.pack(pady=10)

        # --- CAMPOS COMUNES ---
        self.entry_id = ctk.CTkEntry(self, placeholder_text="ID Vehículo (Ej: 1)", width=250)
        self.entry_id.pack(pady=5)
        
        self.entry_patente = ctk.CTkEntry(self, placeholder_text="Patente (Ej: AB123CD)", width=250)
        self.entry_patente.pack(pady=5)
        
        self.entry_marca = ctk.CTkEntry(self, placeholder_text="Marca (Ej: Toyota)", width=250)
        self.entry_marca.pack(pady=5)
        
        self.entry_modelo = ctk.CTkEntry(self, placeholder_text="Modelo (Ej: Corolla)", width=250)
        self.entry_modelo.pack(pady=5)
        
        self.entry_precio = ctk.CTkEntry(self, placeholder_text="Precio por Día (Ej: 15000)", width=250)
        self.entry_precio.pack(pady=5)

        # --- CAMPO ESPECÍFICO (Cambia según el tipo) ---
        self.lbl_especifico = ctk.CTkLabel(self, text="Cantidad de Puertas:")
        self.lbl_especifico.pack(pady=(10, 0))
        
        self.entry_especifico = ctk.CTkEntry(self, placeholder_text="Ej: 4", width=250)
        self.entry_especifico.pack(pady=5)
        
        # --- BOTÓN GUARDAR ---
        self.btn_guardar = ctk.CTkButton(
            self, 
            text="Guardar Vehículo", 
            fg_color="green", 
            hover_color="darkgreen", 
            command=self.guardar_vehiculo
        )
        self.btn_guardar.pack(pady=20)

    # Función que cambia el texto del último campo si elegimos Auto o Moto
    def cambiar_tipo(self, seleccion):
        if seleccion == "Auto":
            self.lbl_especifico.configure(text="Cantidad de Puertas:")
            self.entry_especifico.configure(placeholder_text="Ej: 4")
        else:
            self.lbl_especifico.configure(text="Cilindrada (cc):")
            self.entry_especifico.configure(placeholder_text="Ej: 250")

    def guardar_vehiculo(self):
        # 1. Tomamos los datos
        tipo = self.tipo_var.get()
        id_vehiculo = self.entry_id.get()
        patente = self.entry_patente.get()
        marca = self.entry_marca.get()
        modelo = self.entry_modelo.get()
        precio = self.entry_precio.get()
        dato_especifico = self.entry_especifico.get()
        
        # 2. Validamos que no estén vacíos
        if not all([id_vehiculo, patente, marca, modelo, precio, dato_especifico]):
            messagebox.showwarning("Atención", "Por favor, completá todos los campos.")
            return
            
        # 3. Creamos el objeto (usando try/except por si el usuario pone letras en los números)
        try:
            id_vehiculo = int(id_vehiculo)
            precio = float(precio)
            dato_especifico = int(dato_especifico)
            
            if tipo == "Auto":
                nuevo_vehiculo = Auto(id_vehiculo, patente, marca, modelo, precio, dato_especifico)
            else:
                nuevo_vehiculo = Moto(id_vehiculo, patente, marca, modelo, precio, dato_especifico)
                
            # 4. Lo registramos en el sistema
            self.sistema.registrar_vehiculo(nuevo_vehiculo)
            messagebox.showinfo("Éxito", f"{tipo} {marca} {modelo} registrado correctamente.")
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "El ID, el precio y el dato específico deben ser números.")
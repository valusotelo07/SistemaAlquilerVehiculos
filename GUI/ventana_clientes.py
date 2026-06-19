import customtkinter as ctk
from tkinter import messagebox
from modelos.cliente import Cliente

class VentanaClientes(ctk.CTkToplevel):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema 
        
        self.title("Registrar Nuevo Cliente")
        self.geometry("400x400")
        
        # Estas dos líneas hacen que esta ventana quede siempre por encima de la principal
        self.transient(master)
        self.grab_set()

        # Título interno
        self.lbl_titulo = ctk.CTkLabel(self, text="Datos del Cliente", font=("Arial", 18, "bold"))
        self.lbl_titulo.pack(pady=20)
        
        # --- CAMPOS DE TEXTO ---
        self.entry_id = ctk.CTkEntry(self, placeholder_text="ID Cliente (Ej: 1)", width=250)
        self.entry_id.pack(pady=10)
        
        self.entry_dni = ctk.CTkEntry(self, placeholder_text="DNI (Sin puntos)", width=250)
        self.entry_dni.pack(pady=10)
        
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre", width=250)
        self.entry_nombre.pack(pady=10)
        
        self.entry_apellido = ctk.CTkEntry(self, placeholder_text="Apellido", width=250)
        self.entry_apellido.pack(pady=10)
        
        # --- BOTÓN GUARDAR ---
        self.btn_guardar = ctk.CTkButton(
            self, 
            text="Guardar Cliente", 
            fg_color="green", 
            hover_color="darkgreen", 
            command=self.guardar_cliente
        )
        self.btn_guardar.pack(pady=20)

    def guardar_cliente(self):
        # 1. Tomamos lo que escribió el usuario
        id_cliente = self.entry_id.get()
        dni = self.entry_dni.get()
        nombre = self.entry_nombre.get()
        apellido = self.entry_apellido.get()
        
        # 2. Validamos que no deje nada en blanco
        if not id_cliente or not dni or not nombre or not apellido:
            messagebox.showwarning("Atención", "Por favor, completá todos los campos.")
            return
            
        # 3. Creamos el objeto Cliente y lo registramos en el sistema central
        nuevo_cliente = Cliente(int(id_cliente), dni, nombre, apellido)
        self.sistema.registrar_cliente(nuevo_cliente)
        
        # 4. Avisamos que se guardó y cerramos la ventanita
        messagebox.showinfo("Éxito", f"Cliente {nombre} {apellido} registrado correctamente.")
        self.destroy()
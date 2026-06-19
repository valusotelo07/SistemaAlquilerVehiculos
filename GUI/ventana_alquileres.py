import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from modelos.alquiler import Alquiler
from modelos.comprobante import Comprobante


class VentanaAlquileres(ctk.CTkToplevel):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema
        
        self.title("Generar Nuevo Alquiler")
        self.geometry("450x550") 
        
        self.transient(master)
        self.grab_set()

        self.lbl_titulo = ctk.CTkLabel(self, text="Detalle del Alquiler", font=("Arial", 18, "bold"))
        self.lbl_titulo.pack(pady=(15, 10))

        # --- PREPARAR DATOS PARA LOS MENÚS DESPLEGABLES ---
        clientes = self.sistema.obtener_clientes()
        vehiculos = self.sistema.obtener_vehiculos()

        opciones_clientes = [f"{c.get_dni()} - {c.get_nombre()} {c.get_apellido()}" for c in clientes]
        opciones_vehiculos = [f"{v.get_patente()} - {v.get_marca()} {v.get_modelo()}" for v in vehiculos]

        if not opciones_clientes:
            opciones_clientes = ["(Debes registrar un cliente primero)"]
        if not opciones_vehiculos:
            opciones_vehiculos = ["(Debes registrar un vehículo primero)"]

        # --- SELECTOR DE CLIENTE ---
        self.lbl_cliente = ctk.CTkLabel(self, text="Seleccionar Cliente:")
        self.lbl_cliente.pack(pady=(10, 0))
        
        self.cliente_var = ctk.StringVar(value=opciones_clientes[0])
        self.combo_cliente = ctk.CTkOptionMenu(self, values=opciones_clientes, variable=self.cliente_var, width=250)
        self.combo_cliente.pack(pady=5)

        # --- SELECTOR DE VEHÍCULO ---
        self.lbl_vehiculo = ctk.CTkLabel(self, text="Seleccionar Vehículo:")
        self.lbl_vehiculo.pack(pady=(10, 0))
        
        self.vehiculo_var = ctk.StringVar(value=opciones_vehiculos[0])
        self.combo_vehiculo = ctk.CTkOptionMenu(self, values=opciones_vehiculos, variable=self.vehiculo_var, width=250)
        self.combo_vehiculo.pack(pady=5)

        # --- FECHAS ---
        self.lbl_fechas = ctk.CTkLabel(self, text="Fechas (Formato: DD/MM/AAAA):")
        self.lbl_fechas.pack(pady=(15, 0))
        
        self.entry_inicio = ctk.CTkEntry(self, placeholder_text="Inicio (Ej: 20/07/2026)", width=250)
        self.entry_inicio.pack(pady=5)
        
        self.entry_fin = ctk.CTkEntry(self, placeholder_text="Fin (Ej: 25/07/2026)", width=250)
        self.entry_fin.pack(pady=5)

        # --- BOTÓN GENERAR ALQUILER (Acá está el que faltaba) ---
        self.btn_guardar = ctk.CTkButton(
            self, 
            text="Confirmar Alquiler", 
            fg_color="green", 
            hover_color="darkgreen", 
            command=self.generar_alquiler
        )
        self.btn_guardar.pack(pady=25)

    def generar_alquiler(self):
        seleccion_cliente = self.cliente_var.get()
        seleccion_vehiculo = self.vehiculo_var.get()

        if "(Debes" in seleccion_cliente or "(Debes" in seleccion_vehiculo:
            messagebox.showerror("Error", "Faltan registrar clientes o vehículos en el sistema.")
            return

        str_inicio = self.entry_inicio.get()
        str_fin = self.entry_fin.get()

        try:
            fecha_inicio = datetime.strptime(str_inicio, "%d/%m/%Y").date()
            fecha_fin = datetime.strptime(str_fin, "%d/%m/%Y").date()

            if fecha_fin < fecha_inicio:
                messagebox.showerror("Error", "La fecha de fin no puede ser anterior a la de inicio.")
                return

            dni_cliente = seleccion_cliente.split(" - ")[0]
            patente_vehiculo = seleccion_vehiculo.split(" - ")[0]

            cliente_obj = self.sistema.buscar_cliente_por_dni(dni_cliente)
            vehiculo_obj = self.sistema.buscar_vehiculo_por_patente(patente_vehiculo)

            id_alquiler = len(self.sistema.obtener_alquileres()) + 1

            nuevo_alquiler = Alquiler(id_alquiler, cliente_obj, vehiculo_obj, fecha_inicio, fecha_fin)
            monto = nuevo_alquiler.calcular_monto_total()

            self.sistema.procesar_alquiler(nuevo_alquiler)

            comprobante = Comprobante(id_alquiler, nuevo_alquiler)
            mensaje_exito = comprobante.emitir()
            
            messagebox.showinfo("Comprobante Generado", mensaje_exito)
            self.destroy()
            
            mensaje_exito = (
                f"¡Alquiler #{id_alquiler} registrado con éxito!\n\n"
                f"Cliente: {cliente_obj.get_nombre()} {cliente_obj.get_apellido()}\n"
                f"Vehículo: {vehiculo_obj.get_marca()} {vehiculo_obj.get_modelo()}\n"
                f"Costo Total a cobrar: ${monto:.2f}"
            )
            messagebox.showinfo("Comprobante Generado", mensaje_exito)
            self.destroy()

        except ValueError:
            messagebox.showerror("Error", "Asegurate de escribir las fechas exactamente así: DD/MM/AAAA (ejemplo: 22/07/2026).")
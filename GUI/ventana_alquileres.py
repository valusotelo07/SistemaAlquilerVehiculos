import customtkinter as ctk
from datetime import datetime, date
from modelos.alquiler import Alquiler
from modelos.comprobante import Comprobante

# ==========================================
# CARTEL DE ÉXITO ESTILO "TICKET"
# ==========================================
class VentanaComprobante(ctk.CTkToplevel):
    def __init__(self, master, texto_comprobante):
        super().__init__(master)
        self.title("NovaDrive - Ticket")
        self.geometry("450x450")
        self.transient(master)
        self.grab_set()

        self.lbl_titulo = ctk.CTkLabel(self, text="✅ ¡Alquiler Confirmado!", font=ctk.CTkFont(size=22, weight="bold"), text_color="#2FA572")
        self.lbl_titulo.pack(pady=(25, 10))

        self.ticket_frame = ctk.CTkFrame(self, fg_color="gray15", corner_radius=10)
        self.ticket_frame.pack(padx=30, pady=10, fill="both", expand=True)

        self.lbl_texto = ctk.CTkLabel(self.ticket_frame, text=texto_comprobante, font=("Courier", 14), justify="left")
        self.lbl_texto.pack(padx=20, pady=20)

        self.btn_cerrar = ctk.CTkButton(self, text="Aceptar", fg_color="#1f6aa5", hover_color="#144870", height=40, command=self.destroy)
        self.btn_cerrar.pack(pady=(10, 25))

# ==========================================
# PANEL CENTRAL DE ALQUILERES
# ==========================================
class PanelAlquileres(ctk.CTkFrame):
    def __init__(self, master, sistema):
        super().__init__(master, fg_color="transparent")
        self.sistema = sistema
        
        self.tarjeta = ctk.CTkFrame(self, corner_radius=15)
        self.tarjeta.pack(pady=40, padx=40, fill="both", expand=True)

        self.lbl_titulo = ctk.CTkLabel(self.tarjeta, text="📄 Generar Nuevo Alquiler", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo.pack(pady=(30, 15))

        clientes = self.sistema.obtener_clientes()
        vehiculos = self.sistema.obtener_vehiculos()

        opciones_clientes = [f"{c.get_dni()} - {c.get_nombre()} {c.get_apellido()}" for c in clientes]
        opciones_vehiculos = [f"{v.get_patente()} - {v.get_marca()} {v.get_modelo()}" for v in vehiculos]

        if not opciones_clientes: opciones_clientes = ["(Debes registrar un cliente primero)"]
        if not opciones_vehiculos: opciones_vehiculos = ["(Debes registrar un vehículo primero)"]

        self.cliente_var = ctk.StringVar(value=opciones_clientes[0])
        self.combo_cliente = ctk.CTkOptionMenu(self.tarjeta, values=opciones_clientes, variable=self.cliente_var, width=350, height=40)
        self.combo_cliente.pack(pady=(10, 15))

        self.vehiculo_var = ctk.StringVar(value=opciones_vehiculos[0])
        self.combo_vehiculo = ctk.CTkOptionMenu(self.tarjeta, values=opciones_vehiculos, variable=self.vehiculo_var, width=350, height=40)
        self.combo_vehiculo.pack(pady=15)
        
        self.entry_inicio = ctk.CTkEntry(self.tarjeta, placeholder_text="Inicio (Ej: 20/07/2026)", width=350, height=40)
        self.entry_inicio.pack(pady=15)
        
        self.entry_fin = ctk.CTkEntry(self.tarjeta, placeholder_text="Fin (Ej: 25/07/2026)", width=350, height=40)
        self.entry_fin.pack(pady=15)

        self.btn_guardar = ctk.CTkButton(
            self.tarjeta, text="Confirmar Alquiler", fg_color="#2FA572", hover_color="#217a53", 
            height=45, width=350, font=ctk.CTkFont(weight="bold"), command=self.generar_alquiler
        )
        self.btn_guardar.pack(pady=(20, 10))

        # --- ETIQUETA PARA MENSAJES ---
        self.lbl_mensaje = ctk.CTkLabel(self.tarjeta, text="", font=("Arial", 14, "bold"))
        self.lbl_mensaje.pack(pady=5)

    def generar_alquiler(self):
        seleccion_cliente = self.cliente_var.get()
        seleccion_vehiculo = self.vehiculo_var.get()

        if "(Debes" in seleccion_cliente or "(Debes" in seleccion_vehiculo:
            self.lbl_mensaje.configure(text="❌ Error: Faltan clientes o vehículos.", text_color="#d83a3a")
            return

        str_inicio = self.entry_inicio.get().strip()
        str_fin = self.entry_fin.get().strip()

        try:
            fecha_inicio = datetime.strptime(str_inicio, "%d/%m/%Y").date()
            fecha_fin = datetime.strptime(str_fin, "%d/%m/%Y").date()

            # VALIDACIÓN: Fecha no puede ser anterior a HOY
            if fecha_inicio < date.today():
                self.lbl_mensaje.configure(text="❌ Error: La fecha de inicio no puede ser pasada.", text_color="#d83a3a")
                return

            # VALIDACIÓN: Fecha fin no puede ser anterior a inicio
            if fecha_fin < fecha_inicio:
                self.lbl_mensaje.configure(text="❌ Error: La fecha fin no puede ser anterior al inicio.", text_color="#d83a3a")
                return

            dni_cliente = seleccion_cliente.split(" - ")[0]
            patente_vehiculo = seleccion_vehiculo.split(" - ")[0]

            cliente_obj = self.sistema.buscar_cliente_por_dni(dni_cliente)
            vehiculo_obj = self.sistema.buscar_vehiculo_por_patente(patente_vehiculo)

            id_alquiler = len(self.sistema.obtener_alquileres()) + 1

            nuevo_alquiler = Alquiler(id_alquiler, cliente_obj, vehiculo_obj, fecha_inicio, fecha_fin)
            self.sistema.procesar_alquiler(nuevo_alquiler)
            
            comprobante = Comprobante(id_alquiler, nuevo_alquiler)
            mensaje_exito = comprobante.emitir()
            
            # Limpiamos los campos y el mensaje de error por si había uno
            self.lbl_mensaje.configure(text="")
            self.entry_inicio.delete(0, 'end')
            self.entry_fin.delete(0, 'end')

            VentanaComprobante(self, mensaje_exito)

        except ValueError:
            self.lbl_mensaje.configure(text="❌ Error: Usá el formato DD/MM/AAAA.", text_color="#d83a3a")
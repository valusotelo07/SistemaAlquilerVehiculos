import customtkinter as ctk
import os
from datetime import datetime, date
from modelos.alquiler import Alquiler
from modelos.comprobante import Comprobante

# ==========================================
# VENTANA DE COMPROBANTE
# ==========================================
class VentanaComprobante(ctk.CTkToplevel):
    def __init__(self, master, texto_comprobante):
        super().__init__(master)
        self.title("NovaDrive - Ticket")
        self.geometry("480x520")
        self.transient(master)
        self.grab_set()

        self.lbl_titulo = ctk.CTkLabel(self, text="Alquiler Confirmado", font=ctk.CTkFont(size=22, weight="bold"), text_color="#2FA572")
        self.lbl_titulo.pack(pady=(25, 10))

        self.ticket_frame = ctk.CTkFrame(self, fg_color="gray15", corner_radius=10)
        self.ticket_frame.pack(padx=30, pady=10, fill="both", expand=True)

        self.lbl_texto = ctk.CTkLabel(self.ticket_frame, text=texto_comprobante, font=("Courier", 13), justify="left")
        self.lbl_texto.pack(padx=20, pady=20)

        self.btn_cerrar = ctk.CTkButton(self, text="Aceptar", fg_color="#1f6aa5", hover_color="#144870", height=40, command=self.destroy)
        self.btn_cerrar.pack(pady=(10, 25))

# ==========================================
# PANEL CENTRAL DE ALQUILERES
# ==========================================
class PanelAlquileres(ctk.CTkFrame):
    def __init__(self, master, sistema, sucursal, empleado_activo=None):
        super().__init__(master, fg_color="transparent")
        self.sistema = sistema
        self.sucursal = sucursal
        self.empleado_activo = empleado_activo

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # MITAD IZQUIERDA: FORMULARIO
        # ==========================================
        self.tarjeta = ctk.CTkFrame(self, corner_radius=15)
        self.tarjeta.grid(row=0, column=0, pady=40, padx=(40, 20), sticky="nsew")

        self.lbl_titulo = ctk.CTkLabel(self.tarjeta, text="Generar Nuevo Alquiler", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo.pack(pady=(25, 5))

        emp_nombre = f"{empleado_activo.get_nombre()} {empleado_activo.get_apellido()}" if empleado_activo else "Sin asignar"
        ctk.CTkLabel(self.tarjeta, text=f"Atendido por: {emp_nombre}", font=("Arial", 12), text_color="gray").pack(pady=(0, 10))

        clientes = self.sistema.obtener_clientes()
        vehiculos = self.sistema.obtener_vehiculos()

        opciones_clientes = [f"{c.get_dni()} - {c.get_nombre()} {c.get_apellido()}" for c in clientes]
        opciones_vehiculos = [f"{v.get_patente()} - {v.get_marca()} {v.get_modelo()}" for v in vehiculos if v.esta_activo()]

        if not opciones_clientes: opciones_clientes = ["(Debes registrar un cliente primero)"]
        if not opciones_vehiculos: opciones_vehiculos = ["(Debes registrar un vehiculo primero)"]

        self.cliente_var = ctk.StringVar(value=opciones_clientes[0])
        self.combo_cliente = ctk.CTkOptionMenu(self.tarjeta, values=opciones_clientes, variable=self.cliente_var, width=350, height=40)
        self.combo_cliente.pack(pady=(5, 10))

        self.vehiculo_var = ctk.StringVar(value=opciones_vehiculos[0])
        self.combo_vehiculo = ctk.CTkOptionMenu(self.tarjeta, values=opciones_vehiculos, variable=self.vehiculo_var, width=350, height=40)
        self.combo_vehiculo.pack(pady=10)

        self.entry_inicio = ctk.CTkEntry(self.tarjeta, placeholder_text="Inicio (Ej: 20/07/2026)", width=350, height=40)
        self.entry_inicio.pack(pady=10)

        self.entry_fin = ctk.CTkEntry(self.tarjeta, placeholder_text="Fin (Ej: 25/07/2026)", width=350, height=40)
        self.entry_fin.pack(pady=10)

        self.entry_seguro = ctk.CTkEntry(self.tarjeta, placeholder_text="Seguro/Garantia en $ (opcional, Ej: 5000)", width=350, height=40)
        self.entry_seguro.pack(pady=10)

        self.btn_guardar = ctk.CTkButton(
            self.tarjeta, text="Confirmar Alquiler", fg_color="#2FA572", hover_color="#217a53",
            height=45, width=350, font=ctk.CTkFont(weight="bold"), command=self.generar_alquiler
        )
        self.btn_guardar.pack(pady=(15, 10))

        self.lbl_mensaje = ctk.CTkLabel(self.tarjeta, text="", font=("Arial", 14, "bold"))
        self.lbl_mensaje.pack(pady=5)

        # ==========================================
        # MITAD DERECHA: LISTA VISUAL
        # ==========================================
        self.tarjeta_lista = ctk.CTkFrame(self, corner_radius=15)
        self.tarjeta_lista.grid(row=0, column=1, pady=40, padx=(20, 40), sticky="nsew")

        self.lbl_titulo_lista = ctk.CTkLabel(self.tarjeta_lista, text="Historial de Alquileres", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo_lista.pack(pady=(30, 10))

        self.scroll_lista = ctk.CTkScrollableFrame(self.tarjeta_lista, fg_color="transparent")
        self.scroll_lista.pack(expand=True, fill="both", padx=20, pady=20)

        self.actualizar_lista()

    def generar_alquiler(self):
        seleccion_cliente = self.cliente_var.get()
        seleccion_vehiculo = self.vehiculo_var.get()

        if "(Debes" in seleccion_cliente or "(Debes" in seleccion_vehiculo:
            self.lbl_mensaje.configure(text="Error: Faltan clientes o vehiculos.", text_color="#d83a3a")
            return

        str_inicio = self.entry_inicio.get().strip()
        str_fin = self.entry_fin.get().strip()
        str_seguro = self.entry_seguro.get().strip()

        try:
            fecha_inicio = datetime.strptime(str_inicio, "%d/%m/%Y").date()
            fecha_fin = datetime.strptime(str_fin, "%d/%m/%Y").date()

            if fecha_inicio < date.today():
                self.lbl_mensaje.configure(text="Error: La fecha de inicio no puede ser pasada.", text_color="#d83a3a")
                return

            if fecha_fin < fecha_inicio:
                self.lbl_mensaje.configure(text="Error: La fecha fin no puede ser anterior al inicio.", text_color="#d83a3a")
                return

            seguro = float(str_seguro) if str_seguro else 0.0
            if seguro < 0:
                seguro = 0.0

            dni_cliente = seleccion_cliente.split(" - ")[0]
            patente_vehiculo = seleccion_vehiculo.split(" - ")[0]

            cliente_obj = self.sistema.buscar_cliente_por_dni(dni_cliente)
            vehiculo_obj = self.sistema.buscar_vehiculo_por_patente(patente_vehiculo)

            if cliente_obj is None or vehiculo_obj is None:
                self.lbl_mensaje.configure(text="Error interno: no se encontro el cliente o vehiculo.", text_color="#d83a3a")
                return

            nuevo_alquiler = self.sistema.procesar_alquiler(
                cliente_obj, vehiculo_obj, fecha_inicio, fecha_fin,
                self.sucursal, self.empleado_activo, seguro
            )
            id_alquiler = nuevo_alquiler.get_id_alquiler()

            comprobante = Comprobante(id_alquiler, nuevo_alquiler)
            mensaje_exito = comprobante.emitir()

            try:
                base_dir = os.path.dirname(os.path.dirname(__file__))
                carpeta_tickets = os.path.join(base_dir, "tickets")
                if not os.path.exists(carpeta_tickets):
                    os.makedirs(carpeta_tickets)
                ruta_archivo = os.path.join(carpeta_tickets, f"Ticket_{id_alquiler}.txt")
                with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                    archivo.write(mensaje_exito)
            except Exception as e:
                print(f"Error al guardar el ticket fisico: {e}")

            self.lbl_mensaje.configure(text="")
            self.entry_inicio.delete(0, 'end')
            self.entry_fin.delete(0, 'end')
            self.entry_seguro.delete(0, 'end')

            VentanaComprobante(self, mensaje_exito)
            self.actualizar_lista()

        except ValueError:
            self.lbl_mensaje.configure(text="Error: Usa el formato DD/MM/AAAA y monto numerico.", text_color="#d83a3a")

    def actualizar_lista(self):
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()

        alquileres = self.sistema.obtener_alquileres()

        if not alquileres:
            ctk.CTkLabel(self.scroll_lista, text="Aun no hay alquileres registrados.", text_color="gray").pack(pady=20)
            return

        for a in alquileres:
            fila = ctk.CTkFrame(self.scroll_lista, fg_color=("gray85", "gray20"), corner_radius=8)
            fila.pack(fill="x", pady=5)

            frame_textos = ctk.CTkFrame(fila, fg_color="transparent")
            frame_textos.pack(side="left", fill="both", expand=True)

            estado = "VIGENTE" if not a.esta_devuelto() else "DEVUELTO"
            color_estado = "#2FA572" if not a.esta_devuelto() else "#d83a3a"

            emp = a.get_empleado()
            empleado_str = f"{emp.get_nombre()} {emp.get_apellido()}" if emp else "—"
            cliente = f"{a.get_cliente().get_nombre()} {a.get_cliente().get_apellido()}"
            vehiculo = f"{a.get_vehiculo().get_marca()} {a.get_vehiculo().get_modelo()} ({a.get_vehiculo().get_patente()})"
            fechas = f"{a.get_fecha_inicio().strftime('%d/%m/%Y')} al {a.get_fecha_fin().strftime('%d/%m/%Y')}"
            precio_formateado = f"{a.calcular_monto_total():,.0f}".replace(",", ".")

            texto_principal = f"Alquiler #{a.get_id_alquiler()}  |  {estado}"
            texto_secundario = f"Cliente: {cliente}\nVehiculo: {vehiculo}\nFechas: {fechas}  |  Total: ${precio_formateado}\nEmpleado: {empleado_str}"

            ctk.CTkLabel(frame_textos, text=texto_principal, font=("Arial", 14, "bold"), text_color=color_estado).pack(side="top", anchor="w", padx=15, pady=(10, 0))
            ctk.CTkLabel(frame_textos, text=texto_secundario, font=("Arial", 12), text_color="gray", justify="left").pack(side="top", anchor="w", padx=15, pady=(5, 10))

            if not a.esta_devuelto():
                btn_devolver = ctk.CTkButton(
                    fila, text="Devolver", fg_color="#d83a3a", hover_color="#b02c2c",
                    width=80, height=30, font=ctk.CTkFont(weight="bold"),
                    command=lambda obj=a: self.marcar_como_devuelto(obj)
                )
                btn_devolver.pack(side="right", padx=15)

    def marcar_como_devuelto(self, alquiler):
        alquiler.registrar_devolucion()
        self.actualizar_lista()

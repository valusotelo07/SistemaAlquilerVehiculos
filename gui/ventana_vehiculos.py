import customtkinter as ctk
from modelos.auto import Auto
from modelos.moto import Moto

class DialogEditarVehiculo(ctk.CTkToplevel):
    def __init__(self, master, vehiculo, on_guardar):
        super().__init__(master)
        self.vehiculo = vehiculo
        self.on_guardar = on_guardar

        self.title("Editar Vehiculo")
        self.geometry("380x280")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(self, text="Editar Vehiculo", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25, 5))
        ctk.CTkLabel(self, text=f"{vehiculo.get_marca()} {vehiculo.get_modelo()} — {vehiculo.get_patente()}",
                     font=("Arial", 12), text_color="gray").pack(pady=(0, 15))

        self.entry_precio = ctk.CTkEntry(self, placeholder_text="Precio por dia", width=300, height=40)
        self.entry_precio.insert(0, str(vehiculo.get_precio_por_dia()))
        self.entry_precio.pack(pady=6)

        self.entry_retiro = ctk.CTkEntry(self, placeholder_text="Sucursal de Retiro", width=300, height=40)
        self.entry_retiro.insert(0, vehiculo.get_sucursal_retiro())
        self.entry_retiro.pack(pady=6)

        self.lbl_msg = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.lbl_msg.pack(pady=4)

        ctk.CTkButton(self, text="Guardar Cambios", fg_color="#1f6aa5", hover_color="#144870",
                      height=40, width=300, command=self.guardar).pack(pady=(5, 20))

    def guardar(self):
        precio_str = self.entry_precio.get().strip()
        retiro = self.entry_retiro.get().strip()

        try:
            precio = float(precio_str)
            if precio <= 0:
                raise ValueError
        except ValueError:
            self.lbl_msg.configure(text="El precio debe ser un numero positivo.", text_color="#d83a3a")
            return

        self.vehiculo.set_precio_por_dia(precio)
        self.vehiculo.set_sucursal_retiro(retiro)
        self.on_guardar()
        self.destroy()


class PanelVehiculos(ctk.CTkFrame):
    def __init__(self, master, sistema):
        super().__init__(master, fg_color="transparent")
        self.sistema = sistema

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # MITAD IZQUIERDA: FORMULARIO
        # ==========================================
        self.tarjeta = ctk.CTkFrame(self, corner_radius=15)
        self.tarjeta.grid(row=0, column=0, pady=40, padx=(40, 20), sticky="nsew")

        self.lbl_titulo = ctk.CTkLabel(self.tarjeta, text="Registrar Nuevo Vehiculo", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo.pack(pady=(30, 10))

        self.tipo_var = ctk.StringVar(value="Auto")
        self.opcion_tipo = ctk.CTkOptionMenu(
            self.tarjeta, values=["Auto", "Moto"], variable=self.tipo_var,
            width=300, height=35, command=self.cambiar_tipo
        )
        self.opcion_tipo.pack(pady=(10, 10))

        self.entry_id = ctk.CTkEntry(self.tarjeta, placeholder_text="ID Vehiculo (Ej: 1)", width=300, height=35)
        self.entry_id.pack(pady=5)

        self.entry_patente = ctk.CTkEntry(self.tarjeta, placeholder_text="Patente (Ej: AB123CD)", width=300, height=35)
        self.entry_patente.pack(pady=5)

        self.entry_marca = ctk.CTkEntry(self.tarjeta, placeholder_text="Marca (Ej: Toyota)", width=300, height=35)
        self.entry_marca.pack(pady=5)

        self.entry_modelo = ctk.CTkEntry(self.tarjeta, placeholder_text="Modelo (Ej: Corolla)", width=300, height=35)
        self.entry_modelo.pack(pady=5)

        self.entry_precio = ctk.CTkEntry(self.tarjeta, placeholder_text="Precio por Dia (Ej: 15000)", width=300, height=35)
        self.entry_precio.pack(pady=5)

        self.lbl_especifico = ctk.CTkLabel(self.tarjeta, text="Cantidad de Puertas:")
        self.lbl_especifico.pack(pady=(5, 0))

        self.entry_especifico = ctk.CTkEntry(self.tarjeta, placeholder_text="Ej: 4", width=300, height=35)
        self.entry_especifico.pack(pady=(0, 5))

        self.entry_retiro = ctk.CTkEntry(self.tarjeta, placeholder_text="Sucursal de Retiro (opcional)", width=300, height=35)
        self.entry_retiro.pack(pady=5)

        self.btn_guardar = ctk.CTkButton(
            self.tarjeta, text="Guardar Vehiculo", fg_color="#1f6aa5",
            hover_color="#144870", height=40, width=300,
            font=ctk.CTkFont(weight="bold"), command=self.guardar_vehiculo
        )
        self.btn_guardar.pack(pady=(10, 5))

        self.lbl_mensaje = ctk.CTkLabel(self.tarjeta, text="", font=("Arial", 14, "bold"))
        self.lbl_mensaje.pack(pady=5)

        # ==========================================
        # MITAD DERECHA: LISTA VISUAL
        # ==========================================
        self.tarjeta_lista = ctk.CTkFrame(self, corner_radius=15)
        self.tarjeta_lista.grid(row=0, column=1, pady=40, padx=(20, 40), sticky="nsew")

        self.lbl_titulo_lista = ctk.CTkLabel(self.tarjeta_lista, text="Flota Registrada", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo_lista.pack(pady=(30, 10))

        self.scroll_lista = ctk.CTkScrollableFrame(self.tarjeta_lista, fg_color="transparent")
        self.scroll_lista.pack(expand=True, fill="both", padx=20, pady=20)

        self.actualizar_lista()

    def cambiar_tipo(self, seleccion):
        if seleccion == "Auto":
            self.lbl_especifico.configure(text="Cantidad de Puertas:")
            self.entry_especifico.configure(placeholder_text="Ej: 4")
        else:
            self.lbl_especifico.configure(text="Cilindrada (cc):")
            self.entry_especifico.configure(placeholder_text="Ej: 250")

    def guardar_vehiculo(self):
        tipo = self.tipo_var.get()
        id_vehiculo = self.entry_id.get().strip()
        patente = self.entry_patente.get().strip().upper()
        marca = self.entry_marca.get().strip().upper()
        modelo = self.entry_modelo.get().strip().upper()
        precio = self.entry_precio.get().strip()
        dato_especifico = self.entry_especifico.get().strip()
        retiro = self.entry_retiro.get().strip()

        if not all([id_vehiculo, patente, marca, modelo, precio, dato_especifico]):
            self.lbl_mensaje.configure(text="Por favor, completa todos los campos.", text_color="#e5a50a")
            return

        for v in self.sistema.obtener_vehiculos():
            if str(v.get_id()) == id_vehiculo:
                self.lbl_mensaje.configure(text="Error: El ID de vehiculo ya existe.", text_color="#d83a3a")
                return
            if v.get_patente() == patente:
                self.lbl_mensaje.configure(text="Error: La patente ya esta registrada.", text_color="#d83a3a")
                return

        try:
            id_vehiculo = int(id_vehiculo)
            precio = float(precio)
            dato_especifico = int(dato_especifico)

            if tipo == "Auto":
                nuevo_vehiculo = Auto(id_vehiculo, patente, marca, modelo, precio, dato_especifico, retiro)
            else:
                nuevo_vehiculo = Moto(id_vehiculo, patente, marca, modelo, precio, dato_especifico, retiro)

            self.sistema.registrar_vehiculo(nuevo_vehiculo)
            self.lbl_mensaje.configure(text=f"{tipo} {marca} {modelo} registrado con exito.", text_color="#2FA572")

            self.entry_id.delete(0, 'end')
            self.entry_patente.delete(0, 'end')
            self.entry_marca.delete(0, 'end')
            self.entry_modelo.delete(0, 'end')
            self.entry_precio.delete(0, 'end')
            self.entry_especifico.delete(0, 'end')
            self.entry_retiro.delete(0, 'end')

            self.actualizar_lista()

        except ValueError:
            self.lbl_mensaje.configure(text="Error: ID, precio y dato especifico deben ser numeros.", text_color="#d83a3a")

    def actualizar_lista(self):
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()

        vehiculos = self.sistema.obtener_vehiculos()

        if not vehiculos:
            ctk.CTkLabel(self.scroll_lista, text="Aun no hay vehiculos registrados.", text_color="gray").pack(pady=20)
            return

        for v in vehiculos:
            activo = v.esta_activo()
            color_fila = ("gray85", "gray20") if activo else ("gray75", "gray15")

            fila = ctk.CTkFrame(self.scroll_lista, fg_color=color_fila, corner_radius=8)
            fila.pack(fill="x", pady=5)

            frame_textos = ctk.CTkFrame(fila, fg_color="transparent")
            frame_textos.pack(side="left", fill="both", expand=True)

            if isinstance(v, Auto):
                tipo = "Auto"
                detalle = f"Puertas: {v.get_cantidad_puertas()}"
            else:
                tipo = "Moto"
                detalle = f"Motor: {v.get_cilindrada()}cc"

            retiro = v.get_sucursal_retiro() if v.get_sucursal_retiro() else "Sin definir"
            precio_formateado = f"{v.get_precio_por_dia():,.0f}".replace(",", ".")
            estado_texto = "" if activo else "  [INACTIVO]"
            estado_color = "white" if activo else "#d83a3a"

            texto_principal = f"[{tipo}] {v.get_marca()} {v.get_modelo()} | {v.get_patente()}{estado_texto}"
            texto_secundario = f"ID: {v.get_id()}  —  ${precio_formateado}/dia  —  {detalle}  —  Retiro: {retiro}"

            ctk.CTkLabel(frame_textos, text=texto_principal, font=("Arial", 14, "bold"),
                         text_color=estado_color).pack(anchor="w", padx=15, pady=(10, 0))
            ctk.CTkLabel(frame_textos, text=texto_secundario, font=("Arial", 12),
                         text_color="gray").pack(anchor="w", padx=15, pady=(0, 10))

            frame_botones = ctk.CTkFrame(fila, fg_color="transparent")
            frame_botones.pack(side="right", padx=10, pady=5)

            ctk.CTkButton(
                frame_botones, text="Editar", fg_color="#e5a50a", hover_color="#b07d08",
                text_color="black", width=65, height=28, font=ctk.CTkFont(weight="bold"),
                command=lambda vehiculo=v: self.abrir_editar(vehiculo)
            ).pack(pady=3)

            if activo:
                ctk.CTkButton(
                    frame_botones, text="Baja", fg_color="#d83a3a", hover_color="#b02c2c",
                    width=65, height=28, font=ctk.CTkFont(weight="bold"),
                    command=lambda vehiculo=v: self.dar_de_baja(vehiculo)
                ).pack(pady=3)
            else:
                ctk.CTkButton(
                    frame_botones, text="Eliminar", fg_color="#5a1a1a", hover_color="#3a0a0a",
                    width=65, height=28, font=ctk.CTkFont(weight="bold"),
                    command=lambda vehiculo=v: self.eliminar_vehiculo(vehiculo)
                ).pack(pady=3)

    def abrir_editar(self, vehiculo):
        DialogEditarVehiculo(self, vehiculo, self.actualizar_lista)

    def dar_de_baja(self, vehiculo):
        vehiculo.dar_de_baja()
        self.actualizar_lista()

    def eliminar_vehiculo(self, vehiculo):
        self.sistema.eliminar_vehiculo(vehiculo)
        self.actualizar_lista()

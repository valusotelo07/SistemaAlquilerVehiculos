import customtkinter as ctk
from modelos.auto import Auto
from modelos.moto import Moto

class PanelVehiculos(ctk.CTkFrame):
    def __init__(self, master, sistema):
        super().__init__(master, fg_color="transparent")
        self.sistema = sistema 
        
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # MITAD IZQUIERDA: TU FORMULARIO
        # ==========================================
        self.tarjeta = ctk.CTkFrame(self, corner_radius=15)
        self.tarjeta.grid(row=0, column=0, pady=40, padx=(40, 20), sticky="nsew")

        self.lbl_titulo = ctk.CTkLabel(self.tarjeta, text="🚙 Registrar Nuevo Vehículo", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo.pack(pady=(30, 10))
        
        self.tipo_var = ctk.StringVar(value="Auto")
        self.opcion_tipo = ctk.CTkOptionMenu(
            self.tarjeta, values=["Auto", "Moto"], variable=self.tipo_var,
            width=300, height=35, command=self.cambiar_tipo
        )
        self.opcion_tipo.pack(pady=(10, 10))

        self.entry_id = ctk.CTkEntry(self.tarjeta, placeholder_text="ID Vehículo (Ej: 1)", width=300, height=35)
        self.entry_id.pack(pady=5)
        
        self.entry_patente = ctk.CTkEntry(self.tarjeta, placeholder_text="Patente (Ej: AB123CD)", width=300, height=35)
        self.entry_patente.pack(pady=5)
        
        self.entry_marca = ctk.CTkEntry(self.tarjeta, placeholder_text="Marca (Ej: Toyota)", width=300, height=35)
        self.entry_marca.pack(pady=5)
        
        self.entry_modelo = ctk.CTkEntry(self.tarjeta, placeholder_text="Modelo (Ej: Corolla)", width=300, height=35)
        self.entry_modelo.pack(pady=5)
        
        self.entry_precio = ctk.CTkEntry(self.tarjeta, placeholder_text="Precio por Día (Ej: 15000)", width=300, height=35)
        self.entry_precio.pack(pady=5)

        self.lbl_especifico = ctk.CTkLabel(self.tarjeta, text="Cantidad de Puertas:")
        self.lbl_especifico.pack(pady=(5, 0))
        
        self.entry_especifico = ctk.CTkEntry(self.tarjeta, placeholder_text="Ej: 4", width=300, height=35)
        self.entry_especifico.pack(pady=(0, 10))
        
        self.btn_guardar = ctk.CTkButton(
            self.tarjeta, text="Guardar Vehículo", fg_color="#1f6aa5",
            hover_color="#144870", height=45, width=300,
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

        self.lbl_titulo_lista = ctk.CTkLabel(self.tarjeta_lista, text="📋 Flota Registrada", font=ctk.CTkFont(size=20, weight="bold"))
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
        
        if not all([id_vehiculo, patente, marca, modelo, precio, dato_especifico]):
            self.lbl_mensaje.configure(text="⚠️ Por favor, completá todos los campos.", text_color="#e5a50a")
            return
            
       
        for v in self.sistema.obtener_vehiculos():
            if str(v.get_id()) == id_vehiculo:
                self.lbl_mensaje.configure(text="❌ Error: El ID de vehículo ya existe.", text_color="#d83a3a")
                return
            if v.get_patente() == patente:
                self.lbl_mensaje.configure(text="❌ Error: La patente ya está registrada.", text_color="#d83a3a")
                return

        try:
            id_vehiculo = int(id_vehiculo)
            precio = float(precio)
            dato_especifico = int(dato_especifico)
            
            if tipo == "Auto":
                nuevo_vehiculo = Auto(id_vehiculo, patente, marca, modelo, precio, dato_especifico)
            else:
                nuevo_vehiculo = Moto(id_vehiculo, patente, marca, modelo, precio, dato_especifico)
                
            self.sistema.registrar_vehiculo(nuevo_vehiculo)
            self.lbl_mensaje.configure(text=f"✅ {tipo} {marca} {modelo} registrado con éxito.", text_color="#2FA572")
            
            self.entry_id.delete(0, 'end')
            self.entry_patente.delete(0, 'end')
            self.entry_marca.delete(0, 'end')
            self.entry_modelo.delete(0, 'end')
            self.entry_precio.delete(0, 'end')
            self.entry_especifico.delete(0, 'end')

            
            self.actualizar_lista()
            
        except ValueError:
            self.lbl_mensaje.configure(text="❌ Error: ID, precio y dato específico deben ser números.", text_color="#d83a3a")

    def actualizar_lista(self):
        
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()

        vehiculos = self.sistema.obtener_vehiculos()
        
        
        if not vehiculos:
            ctk.CTkLabel(self.scroll_lista, text="Aún no hay vehículos registrados.", text_color="gray").pack(pady=20)
            return

        
        for v in vehiculos:
            fila = ctk.CTkFrame(self.scroll_lista, fg_color=("gray85", "gray20"), corner_radius=8)
            fila.pack(fill="x", pady=5)
            
           
            if isinstance(v, Auto):
                icono = "🚗"
                detalle = f"Puertas: {v.get_cantidad_puertas()}"
            else:
                icono = "🏍️"
                detalle = f"Motor: {v.get_cilindrada()}cc"

            texto_principal = f"{icono} {v.get_marca()} {v.get_modelo()} | {v.get_patente()}"
    
            precio_formateado = f"{v.get_precio_por_dia():,.0f}".replace(",", ".")
            
            texto_secundario = f"ID: {v.get_id()}  -  ${precio_formateado}/día  -  {detalle}"

            lbl_principal = ctk.CTkLabel(fila, text=texto_principal, font=("Arial", 14, "bold"))
            lbl_principal.pack(side="top", anchor="w", padx=15, pady=(10, 0))

            lbl_secundario = ctk.CTkLabel(fila, text=texto_secundario, font=("Arial", 12), text_color="gray")
            lbl_secundario.pack(side="top", anchor="w", padx=15, pady=(0, 10))
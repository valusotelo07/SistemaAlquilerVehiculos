import customtkinter as ctk
from modelos.cliente import Cliente

class PanelClientes(ctk.CTkFrame):
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

        self.lbl_titulo = ctk.CTkLabel(self.tarjeta, text="👤 Registrar Nuevo Cliente", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo.pack(pady=(30, 20))
        
        self.entry_id = ctk.CTkEntry(self.tarjeta, placeholder_text="ID Cliente (Ej: 1)", width=300, height=40)
        self.entry_id.pack(pady=10)
        
        self.entry_dni = ctk.CTkEntry(self.tarjeta, placeholder_text="DNI (Sin puntos)", width=300, height=40)
        self.entry_dni.pack(pady=10)
        
        self.entry_nombre = ctk.CTkEntry(self.tarjeta, placeholder_text="Nombre", width=300, height=40)
        self.entry_nombre.pack(pady=10)
        
        self.entry_apellido = ctk.CTkEntry(self.tarjeta, placeholder_text="Apellido", width=300, height=40)
        self.entry_apellido.pack(pady=10)
        
        self.btn_guardar = ctk.CTkButton(
            self.tarjeta, text="Guardar Cliente", fg_color="#1f6aa5", hover_color="#144870", 
            height=45, width=300, font=ctk.CTkFont(weight="bold"), command=self.guardar_cliente
        )
        self.btn_guardar.pack(pady=(25, 10))

        self.lbl_mensaje = ctk.CTkLabel(self.tarjeta, text="", font=("Arial", 14, "bold"))
        self.lbl_mensaje.pack(pady=10)

        # ==========================================
        # MITAD DERECHA: LISTA VISUAL
        # ==========================================
        self.tarjeta_lista = ctk.CTkFrame(self, corner_radius=15)
        self.tarjeta_lista.grid(row=0, column=1, pady=40, padx=(20, 40), sticky="nsew")

        self.lbl_titulo_lista = ctk.CTkLabel(self.tarjeta_lista, text="📋 Clientes Registrados", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo_lista.pack(pady=(30, 10))

        self.scroll_lista = ctk.CTkScrollableFrame(self.tarjeta_lista, fg_color="transparent")
        self.scroll_lista.pack(expand=True, fill="both", padx=20, pady=20)

        
        self.actualizar_lista()

    def guardar_cliente(self):
        id_cliente = self.entry_id.get().strip()
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        
        if not id_cliente or not dni or not nombre or not apellido:
            self.lbl_mensaje.configure(text="⚠️ Por favor, completá todos los campos.", text_color="#e5a50a")
            return
            
        for c in self.sistema.obtener_clientes():
            if str(c.get_id()) == id_cliente:
                self.lbl_mensaje.configure(text="❌ Error: El ID ingresado ya existe.", text_color="#d83a3a")
                return
            if c.get_dni() == dni:
                self.lbl_mensaje.configure(text="❌ Error: Este DNI ya está registrado.", text_color="#d83a3a")
                return

        nombre = nombre.title()
        apellido = apellido.title()

        nuevo_cliente = Cliente(int(id_cliente), dni, nombre, apellido)
        self.sistema.registrar_cliente(nuevo_cliente)
        
        self.lbl_mensaje.configure(text=f"✅ Cliente {nombre} {apellido} registrado con éxito.", text_color="#2FA572")
        
        self.entry_id.delete(0, 'end')
        self.entry_dni.delete(0, 'end')
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')

        
        self.actualizar_lista()

    def actualizar_lista(self):
    
        for widget in self.scroll_lista.winfo_children():
            widget.destroy()

        clientes = self.sistema.obtener_clientes()
        
        if not clientes:
            ctk.CTkLabel(self.scroll_lista, text="Aún no hay clientes registrados.", text_color="gray").pack(pady=20)
            return

        for c in clientes:
            fila = ctk.CTkFrame(self.scroll_lista, fg_color=("gray85", "gray20"), corner_radius=8)
            fila.pack(fill="x", pady=5)
            
            texto_cliente = f"ID: {c.get_id()} | {c.get_nombre()} {c.get_apellido()} (DNI: {c.get_dni()})"
            ctk.CTkLabel(fila, text=texto_cliente, font=("Arial", 14)).pack(side="left", padx=15, pady=10)
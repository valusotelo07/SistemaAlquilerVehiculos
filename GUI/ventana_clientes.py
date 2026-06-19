import customtkinter as ctk
from modelos.cliente import Cliente

class PanelClientes(ctk.CTkFrame):
    def __init__(self, master, sistema):
        super().__init__(master, fg_color="transparent")
        self.sistema = sistema 
        
        self.tarjeta = ctk.CTkFrame(self, corner_radius=15)
        self.tarjeta.pack(pady=40, padx=40, fill="both", expand=True)

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
            self.tarjeta, 
            text="Guardar Cliente", 
            fg_color="#1f6aa5",
            hover_color="#144870", 
            height=45,
            width=300,
            font=ctk.CTkFont(weight="bold"),
            command=self.guardar_cliente
        )
        self.btn_guardar.pack(pady=(25, 10))

        # --- ETIQUETA PARA MENSAJES EN PANTALLA ---
        self.lbl_mensaje = ctk.CTkLabel(self.tarjeta, text="", font=("Arial", 14, "bold"))
        self.lbl_mensaje.pack(pady=10)

    def guardar_cliente(self):
        id_cliente = self.entry_id.get().strip()
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        apellido = self.entry_apellido.get().strip()
        
        if not id_cliente or not dni or not nombre or not apellido:
            self.lbl_mensaje.configure(text="⚠️ Por favor, completá todos los campos.", text_color="#e5a50a")
            return
            
        # VALIDACIÓN: Evitar duplicados de ID o DNI
        for c in self.sistema.obtener_clientes():
            if str(c.get_id()) == id_cliente:
                self.lbl_mensaje.configure(text="❌ Error: El ID ingresado ya existe.", text_color="#d83a3a")
                return
            if c.get_dni() == dni:
                self.lbl_mensaje.configure(text="❌ Error: Este DNI ya está registrado.", text_color="#d83a3a")
                return

        # Capitalizar nombres por prolijidad (ej: juan -> Juan)
        nombre = nombre.title()
        apellido = apellido.title()

        nuevo_cliente = Cliente(int(id_cliente), dni, nombre, apellido)
        self.sistema.registrar_cliente(nuevo_cliente)
        
        # Mensaje de éxito en pantalla
        self.lbl_mensaje.configure(text=f"✅ Cliente {nombre} {apellido} registrado con éxito.", text_color="#2FA572")
        
        self.entry_id.delete(0, 'end')
        self.entry_dni.delete(0, 'end')
        self.entry_nombre.delete(0, 'end')
        self.entry_apellido.delete(0, 'end')
import customtkinter as ctk

class VentanaLogin(ctk.CTk):
    def __init__(self, sistema):
        super().__init__()
        self.sistema = sistema
        self.empleado_autenticado = None

        self.title("NovaDrive - Iniciar Sesion")
        self.geometry("420x500")
        self.resizable(False, False)

        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.pack(padx=40, pady=40, fill="both", expand=True)

        ctk.CTkLabel(frame, text="NovaDrive", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(40, 5))
        ctk.CTkLabel(frame, text="Sistema de Alquiler de Vehiculos", font=("Arial", 12), text_color="gray").pack(pady=(0, 30))

        self.entry_usuario = ctk.CTkEntry(frame, placeholder_text="Usuario", width=280, height=45)
        self.entry_usuario.pack(pady=10)

        self.entry_contrasena = ctk.CTkEntry(frame, placeholder_text="Contrasena", width=280, height=45, show="*")
        self.entry_contrasena.pack(pady=10)

        self.btn_ingresar = ctk.CTkButton(
            frame, text="Ingresar", fg_color="#1f6aa5", hover_color="#144870",
            height=45, width=280, font=ctk.CTkFont(weight="bold"),
            command=self.intentar_login
        )
        self.btn_ingresar.pack(pady=(20, 10))

        self.lbl_error = ctk.CTkLabel(frame, text="", font=("Arial", 13), text_color="#d83a3a")
        self.lbl_error.pack(pady=5)

        self.entry_usuario.bind("<Return>", lambda e: self.entry_contrasena.focus())
        self.entry_contrasena.bind("<Return>", lambda e: self.intentar_login())

    def intentar_login(self):
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not contrasena:
            self.lbl_error.configure(text="Completa usuario y contrasena.")
            return

        empleado = self.sistema.verificar_login(usuario, contrasena)
        if empleado:
            self.empleado_autenticado = empleado
            self.destroy()
        else:
            self.lbl_error.configure(text="Usuario o contrasena incorrectos.")
            self.entry_contrasena.delete(0, "end")

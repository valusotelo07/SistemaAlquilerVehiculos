import customtkinter as ctk
from modelos.empleado import Empleado

class DialogEditarEmpleado(ctk.CTkToplevel):
    def __init__(self, master, empleado, on_guardar):
        super().__init__(master)
        self.empleado = empleado
        self.on_guardar = on_guardar

        self.title("Editar Empleado")
        self.geometry("380x340")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(self, text="Editar Empleado", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(25, 5))
        ctk.CTkLabel(self, text=f"Usuario: @{empleado.get_usuario()}", font=("Arial", 12), text_color="gray").pack(pady=(0, 15))

        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre", width=300, height=40)
        self.entry_nombre.insert(0, empleado.get_nombre())
        self.entry_nombre.pack(pady=6)

        self.entry_apellido = ctk.CTkEntry(self, placeholder_text="Apellido", width=300, height=40)
        self.entry_apellido.insert(0, empleado.get_apellido())
        self.entry_apellido.pack(pady=6)

        self.entry_contrasena = ctk.CTkEntry(self, placeholder_text="Nueva contrasena (dejar vacio para no cambiar)", width=300, height=40, show="*")
        self.entry_contrasena.pack(pady=6)

        self.rol_var = ctk.StringVar(value=empleado.get_rol())
        ctk.CTkOptionMenu(self, values=["empleado", "admin"], variable=self.rol_var, width=300, height=40).pack(pady=6)

        self.lbl_msg = ctk.CTkLabel(self, text="", font=("Arial", 12))
        self.lbl_msg.pack(pady=4)

        ctk.CTkButton(self, text="Guardar Cambios", fg_color="#1f6aa5", hover_color="#144870",
                      height=40, width=300, command=self.guardar).pack(pady=(5, 20))

    def guardar(self):
        nombre = self.entry_nombre.get().strip().title()
        apellido = self.entry_apellido.get().strip().title()
        contrasena = self.entry_contrasena.get().strip()
        rol = self.rol_var.get()

        if not nombre or not apellido:
            self.lbl_msg.configure(text="Nombre y apellido son obligatorios.", text_color="#e5a50a")
            return

        self.empleado.set_nombre(nombre)
        self.empleado.set_apellido(apellido)
        self.empleado.set_rol(rol)
        if contrasena:
            self.empleado.set_contrasena(contrasena)

        self.on_guardar()
        self.destroy()


class PanelAdmin(ctk.CTkFrame):
    def __init__(self, master, sistema):
        super().__init__(master, fg_color="transparent")
        self.sistema = sistema

        ctk.CTkLabel(self, text="Panel de Administracion", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))

        self.tabs = ctk.CTkTabview(self, corner_radius=12)
        self.tabs.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.tabs.add("Alquileres")
        self.tabs.add("Empleados")

        self._construir_tab_alquileres()
        self._construir_tab_empleados()

    # ==========================================
    # TAB ALQUILERES
    # ==========================================
    def _construir_tab_alquileres(self):
        tab = self.tabs.tab("Alquileres")

        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self._scroll_alquileres = scroll

        self._actualizar_alquileres()

    def _actualizar_alquileres(self):
        for w in self._scroll_alquileres.winfo_children():
            w.destroy()

        alquileres = self.sistema.obtener_alquileres()
        if not alquileres:
            ctk.CTkLabel(self._scroll_alquileres, text="No hay alquileres registrados.", text_color="gray").pack(pady=20)
            return

        for a in alquileres:
            fila = ctk.CTkFrame(self._scroll_alquileres, fg_color=("gray85", "gray20"), corner_radius=8)
            fila.pack(fill="x", pady=5)

            estado = "VIGENTE" if not a.esta_devuelto() else "DEVUELTO"
            color = "#2FA572" if not a.esta_devuelto() else "#d83a3a"
            emp = a.get_empleado()
            empleado_str = f"{emp.get_nombre()} {emp.get_apellido()}" if emp else "—"
            precio_fmt = f"{a.calcular_monto_total():,.0f}".replace(",", ".")
            seguro_fmt = f"{a.get_seguro():,.0f}".replace(",", ".")

            ctk.CTkLabel(fila, text=f"Alquiler #{a.get_id_alquiler()}  |  {estado}",
                         font=("Arial", 13, "bold"), text_color=color).pack(anchor="w", padx=15, pady=(8, 2))
            ctk.CTkLabel(fila, text=(
                f"Cliente: {a.get_cliente().get_nombre()} {a.get_cliente().get_apellido()} (DNI: {a.get_cliente().get_dni()})\n"
                f"Vehiculo: {a.get_vehiculo().get_marca()} {a.get_vehiculo().get_modelo()} — {a.get_vehiculo().get_patente()}\n"
                f"Fechas: {a.get_fecha_inicio().strftime('%d/%m/%Y')} al {a.get_fecha_fin().strftime('%d/%m/%Y')}\n"
                f"Empleado: {empleado_str}  |  Seguro: ${seguro_fmt}  |  Total: ${precio_fmt}"
            ), font=("Arial", 12), text_color="gray", justify="left").pack(anchor="w", padx=15, pady=(0, 10))

    # ==========================================
    # TAB EMPLEADOS
    # ==========================================
    def _construir_tab_empleados(self):
        tab = self.tabs.tab("Empleados")

        frame_lista = ctk.CTkFrame(tab, corner_radius=10)
        frame_lista.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        ctk.CTkLabel(frame_lista, text="Empleados Registrados", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5))

        self._scroll_empleados = ctk.CTkScrollableFrame(frame_lista, fg_color="transparent", height=200)
        self._scroll_empleados.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self._actualizar_empleados()

        frame_form = ctk.CTkFrame(tab, corner_radius=10)
        frame_form.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkLabel(frame_form, text="Agregar Empleado", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(12, 5))

        campos = ctk.CTkFrame(frame_form, fg_color="transparent")
        campos.pack(padx=20, pady=5, fill="x")
        campos.grid_columnconfigure((0, 1), weight=1)

        self.e_nombre = ctk.CTkEntry(campos, placeholder_text="Nombre", height=35)
        self.e_nombre.grid(row=0, column=0, padx=5, pady=4, sticky="ew")

        self.e_apellido = ctk.CTkEntry(campos, placeholder_text="Apellido", height=35)
        self.e_apellido.grid(row=0, column=1, padx=5, pady=4, sticky="ew")

        self.e_usuario = ctk.CTkEntry(campos, placeholder_text="Usuario", height=35)
        self.e_usuario.grid(row=1, column=0, padx=5, pady=4, sticky="ew")

        self.e_contrasena = ctk.CTkEntry(campos, placeholder_text="Contrasena", height=35, show="*")
        self.e_contrasena.grid(row=1, column=1, padx=5, pady=4, sticky="ew")

        self.rol_var = ctk.StringVar(value="empleado")
        ctk.CTkOptionMenu(campos, values=["empleado", "admin"], variable=self.rol_var, height=35).grid(
            row=2, column=0, padx=5, pady=4, sticky="ew"
        )
        ctk.CTkButton(campos, text="Agregar", fg_color="#1f6aa5", hover_color="#144870",
                      height=35, command=self._agregar_empleado).grid(row=2, column=1, padx=5, pady=4, sticky="ew")

        self.lbl_msg_emp = ctk.CTkLabel(frame_form, text="", font=("Arial", 12))
        self.lbl_msg_emp.pack(pady=(0, 10))

    def _actualizar_empleados(self):
        for w in self._scroll_empleados.winfo_children():
            w.destroy()

        empleados = self.sistema.obtener_empleados()
        if not empleados:
            ctk.CTkLabel(self._scroll_empleados, text="No hay empleados registrados.", text_color="gray").pack(pady=10)
            return

        for e in empleados:
            fila = ctk.CTkFrame(self._scroll_empleados, fg_color=("gray85", "gray20"), corner_radius=6)
            fila.pack(fill="x", pady=3)

            rol_color = "#e5a50a" if e.get_rol() == "admin" else "gray"
            ctk.CTkLabel(fila, text=f"{e.get_nombre()} {e.get_apellido()} — @{e.get_usuario()}",
                         font=("Arial", 13)).pack(side="left", padx=12, pady=8)
            ctk.CTkLabel(fila, text=f"[{e.get_rol().upper()}]",
                         font=("Arial", 11, "bold"), text_color=rol_color).pack(side="left", padx=(0, 10))

            ctk.CTkButton(
                fila, text="Eliminar", fg_color="#d83a3a", hover_color="#b02c2c",
                width=75, height=28, font=ctk.CTkFont(weight="bold"),
                command=lambda emp=e: self._eliminar_empleado(emp)
            ).pack(side="right", padx=(0, 8))

            ctk.CTkButton(
                fila, text="Editar", fg_color="#e5a50a", hover_color="#b07d08", text_color="black",
                width=65, height=28, font=ctk.CTkFont(weight="bold"),
                command=lambda emp=e: self._abrir_editar_empleado(emp)
            ).pack(side="right", padx=4)

    def _abrir_editar_empleado(self, empleado):
        DialogEditarEmpleado(self, empleado, self._actualizar_empleados)

    def _eliminar_empleado(self, empleado):
        self.sistema.eliminar_empleado(empleado)
        self._actualizar_empleados()

    def _agregar_empleado(self):
        nombre = self.e_nombre.get().strip().title()
        apellido = self.e_apellido.get().strip().title()
        usuario = self.e_usuario.get().strip()
        contrasena = self.e_contrasena.get().strip()
        rol = self.rol_var.get()

        if not all([nombre, apellido, usuario, contrasena]):
            self.lbl_msg_emp.configure(text="Completa todos los campos.", text_color="#e5a50a")
            return

        if self.sistema.buscar_empleado_por_usuario(usuario):
            self.lbl_msg_emp.configure(text="Ese usuario ya existe.", text_color="#d83a3a")
            return

        nuevo_id = len(self.sistema.obtener_empleados()) + 1
        nuevo = Empleado(nuevo_id, nombre, apellido, usuario, contrasena, rol)
        self.sistema.registrar_empleado(nuevo)

        self.e_nombre.delete(0, "end")
        self.e_apellido.delete(0, "end")
        self.e_usuario.delete(0, "end")
        self.e_contrasena.delete(0, "end")
        self.rol_var.set("empleado")

        self.lbl_msg_emp.configure(text=f"{nombre} {apellido} agregado.", text_color="#2FA572")
        self._actualizar_empleados()

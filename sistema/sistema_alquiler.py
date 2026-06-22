from datetime import date
from modelos.cliente import Cliente
from modelos.alquiler import Alquiler

class SistemaAlquiler:
    def __init__(self):
        self.__clientes = []
        self.__vehiculos = []
        self.__alquileres = []
        self.__empleados = []

    # --- OPERACIONES DE ALTA ---
    def registrar_cliente(self, cliente):
        self.__clientes.append(cliente)

    def registrar_vehiculo(self, vehiculo):
        self.__vehiculos.append(vehiculo)

    def registrar_empleado(self, empleado):
        self.__empleados.append(empleado)

    def procesar_alquiler(self, cliente, vehiculo, fecha_inicio, fecha_fin, sucursal=None, empleado=None, seguro=0.0):
        id_alquiler = len(self.__alquileres) + 1
        nuevo_alquiler = Alquiler(id_alquiler, cliente, vehiculo, fecha_inicio, fecha_fin, sucursal, empleado, seguro)
        self.__alquileres.append(nuevo_alquiler)
        return nuevo_alquiler

    # --- OPERACIONES DE BÚSQUEDA ---
    def eliminar_cliente(self, cliente):
        self.__clientes.remove(cliente)

    def eliminar_empleado(self, empleado):
        self.__empleados.remove(empleado)

    def eliminar_vehiculo(self, vehiculo):
        self.__vehiculos.remove(vehiculo)

    def buscar_cliente_por_dni(self, dni):
        for cliente in self.__clientes:
            if cliente.get_dni() == dni:
                return cliente
        return None

    def buscar_vehiculo_por_patente(self, patente):
        for vehiculo in self.__vehiculos:
            if vehiculo.get_patente() == patente:
                return vehiculo
        return None

    def buscar_empleado_por_usuario(self, usuario):
        for empleado in self.__empleados:
            if empleado.get_usuario() == usuario:
                return empleado
        return None

    def verificar_login(self, usuario, contrasena):
        empleado = self.buscar_empleado_por_usuario(usuario)
        if empleado and empleado.verificar_contrasena(contrasena):
            return empleado
        return None

    # --- OPERACIONES DE RECORRIDO ---
    def obtener_clientes(self): return self.__clientes
    def obtener_vehiculos(self): return self.__vehiculos
    def obtener_alquileres(self): return self.__alquileres
    def obtener_empleados(self): return self.__empleados

    # --- DISPONIBILIDAD ---
    def verificar_disponibilidad(self):
        hoy = date.today()
        vehiculos_ocupados = {
            alquiler.get_vehiculo().get_id()
            for alquiler in self.__alquileres
            if not alquiler.esta_devuelto()
            and alquiler.get_fecha_inicio() <= hoy <= alquiler.get_fecha_fin()
        }
        return [v for v in self.__vehiculos if v.get_id() not in vehiculos_ocupados and v.esta_activo()]

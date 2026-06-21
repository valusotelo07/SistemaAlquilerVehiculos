from datetime import date
from modelos.cliente import Cliente
from modelos.alquiler import Alquiler

class SistemaAlquiler:
    def __init__(self):
        self.__clientes = []
        self.__vehiculos = []
        self.__alquileres = []

    # --- OPERACIONES DE ALTA ---
    def registrar_cliente(self, cliente):
        self.__clientes.append(cliente)

    def registrar_vehiculo(self, vehiculo):
        self.__vehiculos.append(vehiculo)

    def procesar_alquiler(self, cliente, vehiculo, fecha_inicio, fecha_fin, sucursal=None):
        # El sistema se encarga de generar el ID automáticamente
        id_alquiler = len(self.__alquileres) + 1
        
        # El sistema instancia el Alquiler 
        nuevo_alquiler = Alquiler(id_alquiler, cliente, vehiculo, fecha_inicio, fecha_fin, sucursal)
        
        self.__alquileres.append(nuevo_alquiler)
        
        return nuevo_alquiler

    # --- OPERACIONES DE BÚSQUEDA ---
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

    # --- OPERACIONES DE RECORRIDO ---
    def obtener_clientes(self):
        return self.__clientes

    def obtener_vehiculos(self):
        return self.__vehiculos

    def obtener_alquileres(self):
        return self.__alquileres

    # --- DISPONIBILIDAD ---
    def verificar_disponibilidad(self):
        hoy = date.today()
        vehiculos_ocupados = {
            alquiler.get_vehiculo().get_id()
            for alquiler in self.__alquileres
            if not alquiler.esta_devuelto()
            and alquiler.get_fecha_inicio() <= hoy <= alquiler.get_fecha_fin()
        }
        return [v for v in self.__vehiculos if v.get_id() not in vehiculos_ocupados]

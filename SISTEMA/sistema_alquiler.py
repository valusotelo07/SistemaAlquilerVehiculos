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

    def procesar_alquiler(self, alquiler):
        self.__alquileres.append(alquiler)

    # --- OPERACIONES DE BÚSQUEDA (Esto era lo que faltaba) ---
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
from modelos.cliente import Cliente
from modelos.alquiler import Alquiler

class SistemaAlquiler:

    def __init__(self):
        self.__clientes = []
        self.__vehiculos = []
        self.__alquileres = []

    def registrar_cliente(self, cliente):
        self.__clientes.append(cliente)

    def registrar_vehiculo(self, vehiculo):
        self.__vehiculos.append(vehiculo)

    def procesar_alquiler(self, alquiler):
        self.__alquileres.append(alquiler)

    def obtener_clientes(self):
        return self.__clientes

    def obtener_vehiculos(self):
        return self.__vehiculos

    def obtener_alquileres(self):
        return self.__alquileres
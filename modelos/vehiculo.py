from abc import ABC, abstractmethod

class Vehiculo(ABC):

    def __init__(self, id, patente, marca, modelo, precio_por_dia, sucursal_retiro=""):
        self.__id = id
        self.__patente = patente
        self.__marca = marca
        self.__modelo = modelo
        self.__precio_por_dia = precio_por_dia
        self.__sucursal_retiro = sucursal_retiro
        self.__activo = True

    # Getters
    def get_id(self): return self.__id
    def get_patente(self): return self.__patente
    def get_marca(self): return self.__marca
    def get_modelo(self): return self.__modelo
    def get_precio_por_dia(self): return self.__precio_por_dia
    def get_sucursal_retiro(self): return self.__sucursal_retiro
    def esta_activo(self): return self.__activo

    # Setters
    def set_precio_por_dia(self, precio): self.__precio_por_dia = precio
    def set_sucursal_retiro(self, sucursal): self.__sucursal_retiro = sucursal

    def dar_de_baja(self): self.__activo = False

    @abstractmethod
    def calcular_tarifa(self, dias):
        pass

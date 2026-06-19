from abc import ABC, abstractmethod

class Vehiculo(ABC):

    def __init__(self, id, patente, marca, modelo, precio_por_dia):
        self.__id = id
        self.__patente = patente
        self.__marca = marca
        self.__modelo = modelo
        self.__precio_por_dia = precio_por_dia

    # Getters
    def get_id(self):
        return self.__id

    def get_patente(self):
        return self.__patente

    def get_marca(self):
        return self.__marca

    def get_modelo(self):
        return self.__modelo

    def get_precio_por_dia(self):
        return self.__precio_por_dia

    @abstractmethod
    def calcular_tarifa(self, dias):
        pass
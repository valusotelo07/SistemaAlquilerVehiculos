from modelos.vehiculo import Vehiculo

class Auto(Vehiculo):

    def __init__(self, id, patente, marca, modelo, precio_por_dia, cantidad_puertas, sucursal_retiro=""):
        super().__init__(id, patente, marca, modelo, precio_por_dia, sucursal_retiro)
        self.__cantidad_puertas = cantidad_puertas

    def get_cantidad_puertas(self): return self.__cantidad_puertas

    def calcular_tarifa(self, dias): return self.get_precio_por_dia() * dias

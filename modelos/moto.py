from modelos.vehiculo import Vehiculo

class Moto(Vehiculo):

    def __init__(self, id, patente, marca, modelo, precio_por_dia, cilindrada, sucursal_retiro=""):
        super().__init__(id, patente, marca, modelo, precio_por_dia, sucursal_retiro)
        self.__cilindrada = cilindrada

    def get_cilindrada(self): return self.__cilindrada

    def calcular_tarifa(self, dias): return self.get_precio_por_dia() * dias * 0.9

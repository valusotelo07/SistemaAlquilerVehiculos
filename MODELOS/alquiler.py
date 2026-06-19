class Alquiler:

    def __init__(self, id_alquiler, cliente, vehiculo, fecha_inicio, fecha_fin):
        self.__id_alquiler = id_alquiler
        self.__cliente = cliente
        self.__vehiculo = vehiculo
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin

    def calcular_monto_total(self):
        dias = (self.__fecha_fin - self.__fecha_inicio).days
        return self.__vehiculo.calcular_tarifa(dias)
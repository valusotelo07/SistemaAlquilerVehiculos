from datetime import date

class Comprobante:
    def __init__(self, id_comprobante, alquiler, tipo="ORIGINAL"):
        self.__id_comprobante = id_comprobante
        self.__fecha_emision = date.today()
        self.__alquiler = alquiler
        self.__tipo = tipo

    def get_tipo(self):
        return self.__tipo

    def emitir(self):
        cliente = self.__alquiler.get_cliente()
        vehiculo = self.__alquiler.get_vehiculo()
        monto = self.__alquiler.calcular_monto_total()

        return (
            f"--- COMPROBANTE DE ALQUILER #{self.__id_comprobante} ---\n"
            f"Tipo: {self.__tipo}\n"
            f"Fecha de Emisión: {self.__fecha_emision.strftime('%d/%m/%Y')}\n\n"
            f"Cliente: {cliente.get_nombre()} {cliente.get_apellido()}\n"
            f"Vehículo: {vehiculo.get_marca()} {vehiculo.get_modelo()}\n"
            f"Fechas: {self.__alquiler.get_fecha_inicio().strftime('%d/%m/%Y')} al {self.__alquiler.get_fecha_fin().strftime('%d/%m/%Y')}\n"
            f"-----------------------------------------\n"
            f"TOTAL A COBRAR: ${monto:.2f}\n"
        )

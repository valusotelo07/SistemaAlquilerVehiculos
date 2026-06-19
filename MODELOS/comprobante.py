from datetime import date

class Comprobante:
    def __init__(self, id_comprobante, alquiler):
        self.__id_comprobante = id_comprobante
        self.__fecha_emision = date.today()
        self.__alquiler = alquiler # Recibe el objeto Alquiler, no duplica datos

    def emitir(self):
        # Le pide los datos al alquiler (delegación)
        cliente = self.__alquiler.get_cliente()
        vehiculo = self.__alquiler.get_vehiculo()
        monto = self.__alquiler.calcular_monto_total()

        return (
            f"--- COMPROBANTE DE ALQUILER #{self.__id_comprobante} ---\n"
            f"Fecha de Emisión: {self.__fecha_emision.strftime('%d/%m/%Y')}\n\n"
            f"Cliente: {cliente.get_nombre()} {cliente.get_apellido()}\n"
            f"Vehículo: {vehiculo.get_marca()} {vehiculo.get_modelo()}\n"
            f"Fechas: {self.__alquiler.get_fecha_inicio().strftime('%d/%m/%Y')} al {self.__alquiler.get_fecha_fin().strftime('%d/%m/%Y')}\n"
            f"-----------------------------------------\n"
            f"TOTAL A COBRAR: ${monto:.2f}\n"
        )
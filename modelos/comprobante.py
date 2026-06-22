from datetime import date

class Comprobante:
    def __init__(self, id_comprobante, alquiler, tipo="ORIGINAL"):
        self.__id_comprobante = id_comprobante
        self.__fecha_emision = date.today()
        self.__alquiler = alquiler
        self.__tipo = tipo

    def get_tipo(self): return self.__tipo

    def emitir(self):
        cliente = self.__alquiler.get_cliente()
        vehiculo = self.__alquiler.get_vehiculo()
        monto = self.__alquiler.calcular_monto_total()
        seguro = self.__alquiler.get_seguro()
        empleado = self.__alquiler.get_empleado()
        sucursal_retiro = vehiculo.get_sucursal_retiro()

        tarifa_base = monto - seguro
        empleado_str = f"{empleado.get_nombre()} {empleado.get_apellido()}" if empleado else "Sin asignar"
        retiro_str = sucursal_retiro if sucursal_retiro else "A confirmar"

        return (
            f"--- COMPROBANTE DE ALQUILER #{self.__id_comprobante} ---\n"
            f"Tipo: {self.__tipo}\n"
            f"Fecha de Emisión: {self.__fecha_emision.strftime('%d/%m/%Y')}\n\n"
            f"Cliente: {cliente.get_nombre()} {cliente.get_apellido()}\n"
            f"DNI: {cliente.get_dni()}\n"
            f"Vehículo: {vehiculo.get_marca()} {vehiculo.get_modelo()}\n"
            f"Patente: {vehiculo.get_patente()}\n"
            f"Sucursal de Retiro: {retiro_str}\n"
            f"Fechas: {self.__alquiler.get_fecha_inicio().strftime('%d/%m/%Y')} "
            f"al {self.__alquiler.get_fecha_fin().strftime('%d/%m/%Y')}\n"
            f"Atendido por: {empleado_str}\n"
            f"-----------------------------------------\n"
            f"Tarifa base:      ${tarifa_base:.2f}\n"
            f"Seguro/Garantía:  ${seguro:.2f}\n"
            f"TOTAL A COBRAR:   ${monto:.2f}\n"
        )

class Alquiler:
    def __init__(self, id_alquiler, cliente, vehiculo, fecha_inicio, fecha_fin, sucursal):
        self.__id_alquiler = id_alquiler
        self.__cliente = cliente
        self.__vehiculo = vehiculo
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__sucursal = sucursal
        self.__devuelto = False
        # montoTotal se calcula y almacena al momento de crear el alquiler (ejecución polimórfica)
        self.__monto_total = self.__calcular_monto()

    def __calcular_monto(self):
        dias = (self.__fecha_fin - self.__fecha_inicio).days
        if dias == 0:
            dias = 1
        return self.__vehiculo.calcular_tarifa(dias)

    # --- Getters ---
    def get_id_alquiler(self):
        return self.__id_alquiler

    def get_cliente(self):
        return self.__cliente

    def get_vehiculo(self):
        return self.__vehiculo

    def get_fecha_inicio(self):
        return self.__fecha_inicio

    def get_fecha_fin(self):
        return self.__fecha_fin

    def get_sucursal(self):
        return self.__sucursal

    def esta_devuelto(self):
        return self.__devuelto

    # --- Lógica de negocio ---
    def calcular_monto_total(self):
        return self.__monto_total

    def registrar_devolucion(self):
        self.__devuelto = True

    def __str__(self):
        return f"Alquiler #{self.__id_alquiler} | Cliente: {self.__cliente.get_apellido()} | Patente: {self.__vehiculo.get_patente()}"

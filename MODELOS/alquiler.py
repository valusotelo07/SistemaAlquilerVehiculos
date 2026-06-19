class Alquiler:
    def __init__(self, id_alquiler, cliente, vehiculo, fecha_inicio, fecha_fin):
        # Atributos encapsulados
        self.__id_alquiler = id_alquiler
        self.__cliente = cliente
        self.__vehiculo = vehiculo
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin

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

    # --- Lógica de negocio ---
    def calcular_monto_total(self):
        """
        Calcula la cantidad de días y delega el cálculo del precio al vehículo.
        Ejecución polimórfica: no necesitamos saber si es Auto o Moto.
        """
        dias = (self.__fecha_fin - self.__fecha_inicio).days
        
        # Validación extra: si se alquila y devuelve el mismo día, cobramos 1 día mínimo
        if dias == 0:
            dias = 1
            
        return self.__vehiculo.calcular_tarifa(dias)

    def __str__(self):
        return f"Alquiler #{self.__id_alquiler} | Cliente: {self.__cliente.get_apellido()} | Patente: {self.__vehiculo.get_patente()}"
from sistema.sistema_alquiler import SistemaAlquiler

class Sucursal:

    def __init__(self, id, nombre, direccion):
        self.__id = id
        self.__nombre = nombre
        self.__direccion = direccion
        self.__sistema = SistemaAlquiler()  # composición: la sucursal posee su propio sistema

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_direccion(self):
        return self.__direccion

    def get_sistema(self):
        return self.__sistema
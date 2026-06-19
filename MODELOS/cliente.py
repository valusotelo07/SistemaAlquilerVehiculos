class Cliente:

    def __init__(self, id, dni, nombre, apellido):
        self.__id = id
        self.__dni = dni
        self.__nombre = nombre
        self.__apellido = apellido

    def get_id(self):
        return self.__id

    def get_dni(self):
        return self.__dni

    def get_nombre(self):
        return self.__nombre

    def get_apellido(self):
        return self.__apellido

    def __str__(self):
        return f"{self.__nombre} {self.__apellido}"
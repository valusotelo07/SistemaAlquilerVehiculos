class Cliente:
    def __init__(self, id_cliente, dni, nombre, apellido):
        self.__id = id_cliente
        self.__dni = dni
        self.__nombre = nombre
        self.__apellido = apellido

    @classmethod
    def desde_string(cls, id_cliente, datos_csv):
        """
        Constructor alternativo (Sobrecarga).
        Permite crear un Cliente pasando un string con los datos separados por comas.
        Ejemplo de uso: Cliente.desde_string(1, "38123456,Juan,Perez")
        """
        dni, nombre, apellido = datos_csv.split(',')
        return cls(id_cliente, dni, nombre, apellido)

    # --- Getters ---
    def get_id(self): return self.__id
    def get_dni(self): return self.__dni
    def get_nombre(self): return self.__nombre
    def get_apellido(self): return self.__apellido

    # --- Setters ---
    def set_nombre(self, nombre): self.__nombre = nombre
    def set_apellido(self, apellido): self.__apellido = apellido
    def set_dni(self, dni): self.__dni = dni

    def __str__(self):
        return f"{self.__nombre} {self.__apellido} (DNI: {self.__dni})"

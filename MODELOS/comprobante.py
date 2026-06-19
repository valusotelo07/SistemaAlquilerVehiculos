from datetime import date

class Comprobante:

    def __init__(self, id_comprobante, tipo):
        self.__id_comprobante = id_comprobante
        self.__fecha_emision = date.today()
        self.__tipo = tipo

    def emitir(self):
        return (
            f"Comprobante #{self.__id_comprobante}\n"
            f"Fecha: {self.__fecha_emision}\n"
            f"Tipo: {self.__tipo}"
        )
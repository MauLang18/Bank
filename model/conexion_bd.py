import sqlite3

class Comunicacion():
    def __init__(self):
        self.conexion = sqlite3.connect('bank.db')

    #Metodos de credito

    def insert_credito(self, MontoPrestamo, TasaInteres, FechaInicio, Plazo, EstatusPrestamo, CedulaPrestatario, NombrePrestatario, ApellidoPrestatario):
        cursor = self.conexion.cursor()
        bd = '''INSERT INTO Credito (MontoPrestamo, TasaInteres, FechaInicio, Plazo, EstatusPrestamo, CedulaPrestatario, NombrePrestatario, ApellidoPrestatario)
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}')'''.format(MontoPrestamo, TasaInteres, FechaInicio, Plazo, EstatusPrestamo, CedulaPrestatario, NombrePrestatario, ApellidoPrestatario)
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()
    
    def mostrar_creditos(self):
        cursor = self.conexion.cursor()
        bd = "SELECT * FROM Credito "
        cursor.execute(bd)
        registro = cursor.fetchall()
        return registro
    
    def mostrar_creditos_id(self, id):
        cursor = self.conexion.cursor()
        bd = '''SELECT * FROM Credito WHERE Id = '{}' '''.format(id)
        cursor.execute(bd)
        registro = cursor.fetchone()
        return registro
    
    def eliminar_credito(self, id):
        cursor = self.conexion.cursor()
        bd = '''DELETE FROM Credito WHERE Id = {}'''.format(id)
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()

    def actualizar_credito(self, Id, MontoPrestamo, TasaInteres, FechaInicio, Plazo, EstatusPrestamo, CedulaPrestatario, NombrePrestatario, ApellidoPrestatario):
        cursor = self.conexion.cursor()
        bd = '''UPDATE Credito SET MontoPrestamo='{}', TasaInteres='{}', FechaInicio='{}', Plazo='{}', EstatusPrestamo='{}', CedulaPrestatario='{}', NombrePrestatario='{}', ApellidoPrestatario='{}'
        WHERE Id='{}' '''.format(MontoPrestamo, TasaInteres, FechaInicio, Plazo, EstatusPrestamo, CedulaPrestatario, NombrePrestatario, ApellidoPrestatario, Id)
        cursor.execute(bd)
        a = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        return a
    
    #Metodos de pagos

    def insert_pagos(self, FechaPago, Monto, IDCredito, TipoPago, MetodoPago, EstadoPago):
        cursor = self.conexion.cursor()
        bd = '''INSERT INTO Pago (FechaPago, Monto, IDCredito, TipoPago, MetodoPago, EstadoPago)
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}')'''.format(FechaPago, Monto, IDCredito, TipoPago, MetodoPago, EstadoPago)
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()
    
    def mostrar_pagos(self):
        cursor = self.conexion.cursor()
        bd = "SELECT * FROM Pago "
        cursor.execute(bd)
        registro = cursor.fetchall()
        return registro
    
    def mostrar_pagos_id(self, id):
        cursor = self.conexion.cursor()
        bd = '''SELECT * FROM Pago WHERE Id = '{}' '''.format(id)
        cursor.execute(bd)
        registro = cursor.fetchall()
        return registro
    
    def eliminar_pagos(self, id):
        cursor = self.conexion.cursor()
        bd = '''DELETE FROM Pago WHERE Id = {}'''.format(id)
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()

    def actualizar_pagos(self, Id, FechaPago, Monto, IDCredito, TipoPago, MetodoPago, EstadoPago):
        cursor = self.conexion.cursor()
        bd = '''UPDATE Pago SET FechaPago='{}', Monto='{}' ,IDCredito='{}', TipoPago='{}', MetodoPago='{}', EstadoPago='{}'
        WHERE Id='{}' '''.format(FechaPago, Monto, IDCredito, TipoPago, MetodoPago, EstadoPago, Id)
        cursor.execute(bd)
        a = cursor.rowcount
        self.conexion.commit()
        cursor.close()
        return a
    
    # Metodos de historial

    def insert_historial(self, Movimiento, Monto, Fecha, Identificacion, Actividad):
        cursor = self.conexion.cursor()
        bd = '''INSERT INTO Historial (Movimiento, Monto, Fecha, Identificacion, Actividad)
                VALUES ('{}', '{}', '{}', '{}', '{}')'''.format(Movimiento, Monto, Fecha, Identificacion, Actividad)
        cursor.execute(bd)
        self.conexion.commit()
        cursor.close()
    
    def mostrar_historial(self):
        cursor = self.conexion.cursor()
        bd = "SELECT * FROM Historial "
        cursor.execute(bd)
        registro = cursor.fetchall()
        return registro
    
    def mostrar_historial_id(self, id):
        cursor = self.conexion.cursor()
        bd = '''SELECT * FROM Historial WHERE Id = '{}' '''.format(id)
        cursor.execute(bd)
        registro = cursor.fetchone()
        return registro
    
    #Metodos de login

    def login(self, Cedula, Password):
        cursor = self.conexion.cursor()
        bd = "SELECT * FROM Usuarios WHERE Cedula = '{}' AND Contrasena = '{}'".format(Cedula, Password)
        cursor.execute(bd)
        registro = cursor.fetchone()
        print(registro)
        return registro
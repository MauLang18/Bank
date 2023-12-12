import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from model.conexion_bd import Comunicacion
from datetime import datetime
from reportlab.pdfgen import canvas

class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('login.ui', self)
        
        self.base_datos = Comunicacion()
        self.crearControles()
        self.inicializarControles()
        self.asociarEventos()

    def crearControles(self):
        self.btnLogin = self.findChild(QtWidgets.QPushButton, "btnLogin")
        self.btnCancel = self.findChild(QtWidgets.QPushButton, "btnCancel")
        self.txtUsername = self.findChild(QtWidgets.QLineEdit, "txtUsername")
        self.txtPassword = self.findChild(QtWidgets.QLineEdit, "txtPassword")

    def inicializarControles(self):
        self.txtUsername.clear()
        self.txtPassword.clear()
    
    def asociarEventos(self):
        self.btnLogin.clicked.connect(self.login)
        self.btnCancel.clicked.connect(self.cancel)

    def login(self):
        username = self.txtUsername.text()  
        password = self.txtPassword.text()  

        user = self.base_datos.login(username, password)
        
        if user:
            print('Inicio de sesión exitoso')
            self.close()  
            self.accept()
        else:
            print('Error de inicio de sesión')
    
    def cancel(self):
        QtWidgets.QApplication.quit()

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super(VentanaPrincipal, self).__init__()
        loadUi("main.ui",self)

        self.base_datos = Comunicacion()
        self.crearControles()
        self.inicializarControles()
        self.asociarEventos()
        self.mostrarCredito()
        self.mostrarPago()
        self.mostrarHistorial()

        self.contador_guardado_pdf = 1
        self.contador_guardado_txt = 1

    #Metodos generales

    def crearControles(self):
        #Menu
        self.btnCredito = self.findChild(QtWidgets.QPushButton, "btnCredito")
        self.btnPago = self.findChild(QtWidgets.QPushButton, "btnPago")
        self.btnHistorial = self.findChild(QtWidgets.QPushButton, "btnHistorial")
        self.btnImprimirPDF = self.findChild(QtWidgets.QPushButton, "btnImprimirPDF")
        self.btnImprimirTXT = self.findChild(QtWidgets.QPushButton, "btnImprimirTXT")
        #Pantalla de credito
        self.btnAgregarCredito = self.findChild(QtWidgets.QPushButton, "btnAgregarCredito")        
        self.btnModificarCredito = self.findChild(QtWidgets.QPushButton, "btnModificarCredito")        
        self.btnEliminarCredito = self.findChild(QtWidgets.QPushButton, "btnEliminarCredito")        
        self.tblCredito = self.findChild(QtWidgets.QTableWidget, "tblCredito")        
        self.txtMontoCredito = self.findChild(QtWidgets.QLineEdit, "txtMontoCredito")       
        self.txtTasaCredito = self.findChild(QtWidgets.QLineEdit, "txtTasaCredito")    
        self.txtPlazoCredito = self.findChild(QtWidgets.QLineEdit, "txtPlazoCredito") 
        self.txtCedulaCredito = self.findChild(QtWidgets.QLineEdit, "txtCedulaCredito") 
        self.txtNombreCredito = self.findChild(QtWidgets.QLineEdit, "txtNombreCredito") 
        self.txtApellidoCredito = self.findChild(QtWidgets.QLineEdit, "txtApellidoCredito") 
        self.cbxEstatusCredito = self.findChild(QtWidgets.QComboBox, "cbxEstatusCredito")    
        self.dteFechaCredito = self.findChild(QtWidgets.QDateTimeEdit, "dteFechaCredito")
        #Pantalla de pagos
        self.btnAgregarPago = self.findChild(QtWidgets.QPushButton, "btnAgregarPago")        
        self.btnModificarPago = self.findChild(QtWidgets.QPushButton, "btnModificarPago")        
        self.btnEliminarPago = self.findChild(QtWidgets.QPushButton, "btnEliminarPago")        
        self.tblPago = self.findChild(QtWidgets.QTableWidget, "tblPago")        
        self.dteFechaPago = self.findChild(QtWidgets.QDateTimeEdit, "dteFechaPago")       
        self.txtMontoPago = self.findChild(QtWidgets.QLineEdit, "txtMontoPago")    
        self.txtIdCreditoPago = self.findChild(QtWidgets.QLineEdit, "txtIdCreditoPago") 
        self.cbxTipoPago = self.findChild(QtWidgets.QComboBox, "cbxTipoPago")
        self.cbxMetodoPago = self.findChild(QtWidgets.QComboBox, "cbxMetodoPago")
        self.cbxEstadoPago = self.findChild(QtWidgets.QComboBox, "cbxEstadoPago")
        #Pantalla de historial
        self.tblHistorial = self.findChild(QtWidgets.QTableWidget, "tblHistorial") 
     
    def inicializarControles(self):
        #Creditos
        self.txtMontoCredito.clear()
        self.txtTasaCredito.clear()
        self.txtPlazoCredito.clear()
        self.txtCedulaCredito.clear()
        self.txtNombreCredito.clear()
        self.txtApellidoCredito.clear()
        self.cbxEstatusCredito.setCurrentIndex(0)
        self.dteFechaCredito.setDate(QtCore.QDate.currentDate()) 
        #Pago
        self.txtMontoPago.clear()
        self.txtIdCreditoPago.clear()
        self.cbxTipoPago.setCurrentIndex(0)
        self.cbxMetodoPago.setCurrentIndex(0)
        self.cbxEstadoPago.setCurrentIndex(0)
        self.dteFechaPago.setDate(QtCore.QDate.currentDate()) 

    def asociarEventos(self):
        #Menu
        self.btnCredito.clicked.connect(self.mostrarPaginaCredito)
        self.btnPago.clicked.connect(self.mostrarPaginaPago)
        self.btnHistorial.clicked.connect(self.mostrarPaginaHistorial)
        self.btnImprimirPDF.clicked.connect(self.imprimirPDF)
        self.btnImprimirTXT.clicked.connect(self.imprimirTXT)
        #Pantalla de creditos
        self.btnAgregarCredito.clicked.connect(self.registrarCredito)
        self.btnModificarCredito.clicked.connect(self.modificarCredito)
        self.btnEliminarCredito.clicked.connect(self.eliminarCredito)
        self.tblCredito.clicked.connect(self.seleccionarDatosCreditos)
        self.tblCredito.clicked.connect(self.mostrarCredito)
        #Pantalla de pagos
        self.btnAgregarPago.clicked.connect(self.registrarPago)
        self.btnModificarPago.clicked.connect(self.modificarPago)
        self.btnEliminarPago.clicked.connect(self.eliminarPago)
        self.tblPago.clicked.connect(self.seleccionarDatosPagos)
        self.tblPago.clicked.connect(self.mostrarPago)
        #Pantalla de historial
        self.tblHistorial.clicked.connect(self.mostrarHistorial)

    def msgProceso(self, textoMensaje, tipoMensaje):        
        titulo = None
        msg = QtWidgets.QMessageBox(self)
        icono = None
        if tipoMensaje == 'I':
            titulo = "Informativo"
            icono = QtWidgets.QMessageBox.Icon.Information
        if tipoMensaje == 'E':
            titulo = "Error"
            icono = QtWidgets.QMessageBox.Icon.Critical
        
        msg.setIcon(icono)
        msg.setWindowTitle(titulo)        
        msg.setText(textoMensaje)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg.exec()

    #Metodos del menu

    def mostrarPaginaCredito(self):
        self.stackedWidget.setCurrentIndex(0)

    def mostrarPaginaPago(self):
        self.stackedWidget.setCurrentIndex(1)

    def mostrarPaginaHistorial(self):
        self.stackedWidget.setCurrentIndex(2)

    def generar_nombre_archivo_pdf(self, tabla):
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{tabla}_{fecha_actual}_{self.contador_guardado_pdf}.pdf"
        self.contador_guardado_pdf += 1
        return nombre_archivo

    def generar_nombre_archivo_txt(self, tabla):
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{tabla}_{fecha_actual}_{self.contador_guardado_txt}.txt"
        self.contador_guardado_txt += 1
        return nombre_archivo

    def imprimirPDF(self):
        self.generar_archivo_pdf('creditos')
        self.generar_archivo_pdf('pagos')
        self.generar_archivo_pdf('historial')
        self.msgProceso(f"Archivos PDF generados exitosamente.", 'I')

    def generar_archivo_pdf(self, tabla):
        nombre_archivo = self.generar_nombre_archivo_pdf(tabla)
        try:
            pdf = canvas.Canvas(nombre_archivo)
            datos = self.obtener_datos_tabla(tabla)
            x = 50
            y = 800
            for row in datos:
                pdf.drawString(x, y, f"ID: {row[0]}, Monto: {row[1]}, Tasa: {row[2]}, Fecha: {row[3]}")
                y -= 20 
            pdf.save()
        except Exception as e:
            self.msgProceso(f"Error al generar archivo PDF: {str(e)}", 'E')

    def obtener_datos_tabla(self, tabla):
        if tabla == 'creditos':
            return self.base_datos.mostrar_creditos()
        elif tabla == 'pagos':
            return self.base_datos.mostrar_pagos()
        elif tabla == 'historial':
            return self.base_datos.mostrar_historial()
        else:
            return [] 

    def imprimirTXT(self):
        self.generar_archivo_txt('creditos')
        self.generar_archivo_txt('pagos')
        self.generar_archivo_txt('historial')
        self.msgProceso(f"Archivos TXT generados exitosamente.", 'I')

    def generar_archivo_txt(self, tabla):
        nombre_archivo = self.generar_nombre_archivo_txt(tabla)
        try:
            with open(nombre_archivo, 'w') as archivo_txt:
                datos = self.obtener_datos_tabla(tabla)
                for row in datos:
                    archivo_txt.write(f"ID: {row[0]}, Monto: {row[1]}, Tasa: {row[2]}, Fecha: {row[3]}\n")
        except Exception as e:
            self.msgProceso(f"Error al generar archivo TXT: {str(e)}", 'E')

    def obtener_datos_tabla(self, tabla):
        if tabla == 'creditos':
            return self.base_datos.mostrar_creditos()
        elif tabla == 'pagos':
            return self.base_datos.mostrar_pagos()
        elif tabla == 'historial':
            return self.base_datos.mostrar_historial()
        else:
            return []

    #Metodos de pagina de creditos

    def mostrarCredito(self):
        datos = self.base_datos.mostrar_creditos()
        i = len(datos)
        self.tblCredito.setRowCount(i)
        tablerow = 0
        for row in datos:
            self.Id = row[0]
            self.tblCredito.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tblCredito.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.tblCredito.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tblCredito.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tblCredito.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.tblCredito.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.tblCredito.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            self.tblCredito.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(row[7])))
            self.tblCredito.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(row[8])))   
            tablerow += 1

    def registrarCredito(self):
        MontoPrestamo = self.txtMontoCredito.text()
        TasaInteres = self.txtTasaCredito.text()
        FechaInicio = self.dteFechaCredito.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        Plazo = self.txtPlazoCredito.text()
        EstatusPrestamo = self.cbxEstatusCredito.currentText()
        CedulaPrestatario = self.txtCedulaCredito.text()
        NombrePrestatario = self.txtNombreCredito.text()
        ApellidoPrestatario = self.txtApellidoCredito.text()

        if MontoPrestamo != '' and TasaInteres != '' and FechaInicio != '' and Plazo != '' and EstatusPrestamo != '' and CedulaPrestatario != '' and NombrePrestatario != '' and ApellidoPrestatario != '':
            self.base_datos.insert_credito(MontoPrestamo,TasaInteres,FechaInicio,Plazo,EstatusPrestamo,CedulaPrestatario,NombrePrestatario,ApellidoPrestatario)
            self.mostrarCredito()
            self.msgProceso("Credito registrado con éxito.", 'I')

            self.base_datos.insert_historial('Credito', MontoPrestamo, FechaInicio, CedulaPrestatario, 'Insercion')
            self.mostrarHistorial()

            self.inicializarControles()
        else:
            self.msgProceso("Hay espacios vacios.", 'E')

    def modificarCredito(self):
        fila_seleccionada = self.tblCredito.currentRow()
        if fila_seleccionada >= 0:  
            id_seleccionado = self.tblCredito.item(fila_seleccionada, 0).text() 

            nuevo_monto = self.txtMontoCredito.text()
            nueva_tasa = self.txtTasaCredito.text()
            nueva_fecha = self.dteFechaCredito.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            nuevo_plazo = self.txtPlazoCredito.text()
            nuevo_estatus = self.cbxEstatusCredito.currentText()
            nueva_cedula = self.txtCedulaCredito.text()
            nuevo_nombre = self.txtNombreCredito.text()
            nuevo_apellido = self.txtApellidoCredito.text()

            if (nuevo_monto and nueva_tasa and nueva_fecha and nuevo_plazo and nuevo_estatus
                    and nueva_cedula and nuevo_nombre and nuevo_apellido):
                self.base_datos.actualizar_credito(id_seleccionado, nuevo_monto, nueva_tasa, nueva_fecha,
                                              nuevo_plazo, nuevo_estatus, nueva_cedula, nuevo_nombre, nuevo_apellido)
                self.mostrarCredito()
                self.msgProceso("Crédito modificado con éxito.", 'I')

                self.base_datos.insert_historial('Credito', nuevo_monto, nueva_fecha, nueva_cedula, 'Actualizacion')
                self.mostrarHistorial()

                self.inicializarControles()
            else:
                self.msgProceso("Complete todos los campos para modificar el crédito.", 'E')
        else:
            self.msgProceso("Seleccione un crédito para modificar.", 'E')

    def eliminarCredito(self):
        fila_seleccionada = self.tblCredito.currentRow()
        if fila_seleccionada >= 0: 
            id_seleccionado = self.tblCredito.item(fila_seleccionada, 0).text() 

            self.base_datos.eliminar_credito(id_seleccionado)
            self.mostrarCredito() 
            self.msgProceso("Crédito eliminado con éxito.", 'I')
            self.inicializarControles()
        else:
            self.msgProceso("Seleccione un crédito para eliminar.", 'E')

    def seleccionarDatosCreditos(self):
        fila_seleccionada = self.tblCredito.currentRow()

        if fila_seleccionada >= 0:
            monto = self.tblCredito.item(fila_seleccionada, 1).text()
            tasa = self.tblCredito.item(fila_seleccionada, 2).text()
            fecha = self.tblCredito.item(fila_seleccionada, 3).text()
            plazo = self.tblCredito.item(fila_seleccionada, 4).text()
            estatus = self.tblCredito.item(fila_seleccionada, 5).text()
            cedula = self.tblCredito.item(fila_seleccionada, 6).text()
            nombre = self.tblCredito.item(fila_seleccionada, 7).text()
            apellido = self.tblCredito.item(fila_seleccionada, 8).text()

            self.txtMontoCredito.setText(monto)
            self.txtTasaCredito.setText(tasa)
            self.dteFechaCredito.setDateTime(QtCore.QDateTime.fromString(fecha, "yyyy-MM-dd HH:mm:ss"))
            self.txtPlazoCredito.setText(plazo)
            self.cbxEstatusCredito.setCurrentText(estatus)
            self.txtCedulaCredito.setText(cedula)
            self.txtNombreCredito.setText(nombre)
            self.txtApellidoCredito.setText(apellido)
        else:
            self.inicializarControles()

    #Metodos de pagina de pagos

    def mostrarPago(self):
        datos = self.base_datos.mostrar_pagos()
        i = len(datos)
        self.tblPago.setRowCount(i)
        tablerow = 0
        for row in datos:
            self.Id = row[0]
            self.tblPago.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tblPago.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.tblPago.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tblPago.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tblPago.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.tblPago.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5]))) 
            self.tblPago.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6]))) 
            tablerow += 1

    def registrarPago(self):
        FechaPago = self.dteFechaPago.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        Monto = self.txtMontoPago.text()
        IDCredito = self.txtIdCreditoPago.text()
        TipoPago = self.cbxTipoPago.currentText()
        MetodoPago = self.cbxMetodoPago.currentText()
        EstadoPago = self.cbxEstadoPago.currentText()

        if FechaPago != '' and Monto != '' and IDCredito != '' and TipoPago != '' and MetodoPago != '' and EstadoPago != '':
            self.base_datos.insert_pagos(FechaPago,Monto,IDCredito,TipoPago,MetodoPago,EstadoPago)
            self.mostrarPago()
            self.msgProceso("Pago registrado con éxito.", 'I')

            self.base_datos.insert_historial('Pago', Monto, FechaPago, IDCredito, 'Insercion')
            self.mostrarHistorial()

            self.inicializarControles()
        else:
            self.msgProceso("Hay espacios vacios.", 'E')

    def modificarPago(self):
        fila_seleccionada = self.tblPago.currentRow()
        if fila_seleccionada >= 0:  
            id_seleccionado = self.tblPago.item(fila_seleccionada, 0).text() 

            nueva_fecha = self.dteFechaPago.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            nuevo_monto = self.txtMontoPago.text()
            nuevo_idCredito = self.txtIdCreditoPago.text()
            nuevo_tipoPago = self.cbxTipoPago.currentText()
            nuevo_metodoPago = self.cbxMetodoPago.currentText()
            nuevo_estadoPago = self.cbxEstadoPago.currentText()

            if (nueva_fecha and nuevo_monto and nuevo_idCredito and nuevo_tipoPago and nuevo_metodoPago
                    and nuevo_estadoPago):
                self.base_datos.actualizar_pagos(id_seleccionado, nueva_fecha, nuevo_monto, nuevo_idCredito,
                                              nuevo_tipoPago, nuevo_metodoPago, nuevo_estadoPago)
                self.mostrarPago()
                self.msgProceso("Pago modificado con éxito.", 'I')
                
                self.base_datos.insert_historial('Pago', nuevo_monto, nueva_fecha, nuevo_idCredito, 'Actualizacion')
                self.mostrarHistorial()

                self.inicializarControles()
            else:
                self.msgProceso("Complete todos los campos para modificar el pago.", 'E')
        else:
            self.msgProceso("Seleccione un pago para modificar.", 'E')

    def eliminarPago(self):
        fila_seleccionada = self.tblPago.currentRow()
        if fila_seleccionada >= 0: 
            id_seleccionado = self.tblPago.item(fila_seleccionada, 0).text() 

            self.base_datos.eliminar_pagos(id_seleccionado)
            self.mostrarPago() 
            self.msgProceso("Pago eliminado con éxito.", 'I')
            self.inicializarControles()
        else:
            self.msgProceso("Seleccione un pago para eliminar.", 'E')

    def seleccionarDatosPagos(self):
        fila_seleccionada = self.tblPago.currentRow()

        if fila_seleccionada >= 0:
            fecha = self.tblPago.item(fila_seleccionada, 1).text()
            monto = self.tblPago.item(fila_seleccionada, 2).text()
            idCredito = self.tblPago.item(fila_seleccionada, 3).text()
            tipoPago = self.tblPago.item(fila_seleccionada, 4).text()
            metodoPago = self.tblPago.item(fila_seleccionada, 5).text()
            estadoPago = self.tblPago.item(fila_seleccionada, 6).text()

            self.dteFechaPago.setDateTime(QtCore.QDateTime.fromString(fecha, "yyyy-MM-dd HH:mm:ss"))
            self.txtMontoPago.setText(monto)
            self.txtIdCreditoPago.setText(idCredito)
            self.cbxTipoPago.setCurrentText(tipoPago)
            self.cbxMetodoPago.setCurrentText(metodoPago)
            self.cbxEstadoPago.setCurrentText(estadoPago)
        else:
            self.inicializarControles()

    #Metodos de pagina de historial

    def mostrarHistorial(self):
        datos = self.base_datos.mostrar_historial()
        i = len(datos)
        self.tblHistorial.setRowCount(i)
        tablerow = 0
        for row in datos:
            self.Id = row[0]
            self.tblHistorial.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tblHistorial.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            self.tblHistorial.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tblHistorial.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tblHistorial.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4]))) 
            self.tblHistorial.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5]))) 
            tablerow += 1

def main():
    app = QApplication(sys.argv)
    login_window = LoginForm()
    login_window.show()

    # Ejemplo de verificación de inicio de sesión
    if login_window.exec_() == LoginForm.Accepted:
        main_window = VentanaPrincipal()
        main_window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
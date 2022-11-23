# @autor: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren

import sys
import time
from PyQt5 import QtCore
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QPushButton,QMessageBox
from DeteccionLaser import DeteccionLaser


class MiApp(QtWidgets.QMainWindow):
	def __init__(self):
		super(MiApp,self).__init__()
		loadUi('menu.ui',self)
		
		#Botones de barra lateral
		
		#eliminar barra y de titulo - opacidad
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setWindowOpacity(1)

		#SizeGrip
		self.gripSize = 10
		self.grip = QtWidgets.QSizeGrip(self)
		self.grip.resize(self.gripSize, self.gripSize)

		# mover ventana
		self.frame_superior.mouseMoveEvent = self.mover_ventana

		#acceder a las paginas
		self.bt_configuracion.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))			
		self.bt_uno.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_uno))	
		self.bt_dos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_tres))	
		self.bt_tres.clicked.connect(lambda: self.close())	
		self.pushButton_10.clicked.connect(self.comenzar_prueba)

		#control barra de titulos
		self.bt_minimizar.clicked.connect(self.control_bt_minimizar)		
		self.bt_restaurar.clicked.connect(self.control_bt_normal)
		self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
		self.bt_cerrar.clicked.connect(lambda: self.close())

		self.bt_restaurar.hide()

		#menu lateral
		self.bt_menu.clicked.connect(self.mover_menu)

	def comenzar_prueba(self):
		self.stackedWidget.setCurrentWidget(self.page_2)
		self.deteccion=DeteccionLaser()
		self.matrizCalibracion=self.deteccion.calibrar()
		QMessageBox.about(self, "Calibracion culminada", "Se ha realizado con exito la calibracion")
		self.mostrar_bull()

	def mostrar_bull(self):
		self.stackedWidget.setCurrentWidget(self.page_3)
		CoordenadaX, CoordenadaY, imgDeteccion=self.deteccion.encontrarPunto()
		CoordenadaProy, imgTransformada=self.deteccion.obtenerPuntoProyectado(self.matrizCalibracion, imgDeteccion, CoordenadaX, CoordenadaY)


	def control_bt_minimizar(self):
		self.showMinimized()		

	def  control_bt_normal(self): 
		self.showNormal()		
		self.bt_restaurar.hide()
		self.bt_maximizar.show()

	def  control_bt_maximizar(self): 
		self.showMaximized()
		self.bt_maximizar.hide()
		self.bt_restaurar.show()

	def mover_menu(self):
		if True:			
			width = self.frame_lateral.width()
			normal = 0
			if width==0:
				extender = 200
			else:
				extender = normal
			self.animacion = QPropertyAnimation(self.frame_lateral, b'minimumWidth')
			self.animacion.setDuration(300)
			self.animacion.setStartValue(width)
			self.animacion.setEndValue(extender)
			self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
			self.animacion.start()

	## SizeGrip
	def resizeEvent(self, event):
		rect = self.rect()
		self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

	## mover ventana
	def mousePressEvent(self, event):
		self.clickPosition = event.globalPos()

	def mover_ventana(self, event):
		if self.isMaximized() == False:			
			if event.buttons() == QtCore.Qt.LeftButton:
				self.move(self.pos() + event.globalPos() - self.clickPosition)
				self.clickPosition = event.globalPos()
				event.accept()

		if event.globalPos().y() <=20:
			self.showMaximized()
		else:
			self.showNormal()

class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Calibracion exitosa")
        self.setFixedSize(200, 100)
			

if __name__ == "__main__":
     app = QtWidgets.QApplication(sys.argv)
     mi_app = MiApp()
     mi_app.show()
     sys.exit(app.exec_())	



from PyQt6.QtWidgets import *
from PyQt6 import QtCore
from PyQt6.QtGui import QFont, QIcon, QMovie
from PyQt6.QtCore import QSize
import sys

class MyWindow(QWidget):
    def __init__(self):
        super(). __init__()
                        #posx, posy, width, height inicial
        self.setGeometry(250, 500, 640, 480)
        self.setWindowTitle("Nome_do_app")
        self.setWindowIcon(QIcon("icone.bmp"))
        self.setMaximumHeight(600) #maxima altura da janela
        self.setMaximumWidth(800)   #maxima largura da janela
        self.setMinimumHeight(480)  #minima altura da janela
        self.setMinimumWidth(640)   #minima largura da janela
        self.create_widgets()
    
    def create_widgets(self):
        self.container_widget = QWidget()
        self.btn = QPushButton("Lutar")
        self.btn.clicked.connect(self.fight_btn)
        self.btn_2 = QPushButton("Bolsa")
        self.btn_2.clicked.connect(self.bag_btn)
        self.btn_3 = QPushButton("Fugir")
        self.btn_3.clicked.connect(self.run_btn)
        self.label = QLabel("O que o jogador irá fazer?")
        self.label.setFixedSize(200, 50)
        
        self.grid_menu = QGridLayout()
        self.grid_menu.addWidget(self.btn,0,1)
        self.grid_menu.addWidget(self.btn_2,0,2)
        self.grid_menu.addWidget(self.btn_3,1,1)
        self.grid_menu.addWidget(self.label,0,0)
        self.setLayout(self.grid_menu)
         

    def menu(self):
        self.setLayout(self.grid_menu)


    def fight_btn(self):
        self.grid_luta = QGridLayout()
        self.grid_luta.addWidget(self.btn,0,1)
        self.btn.clicked.connect(self.menu)
        self.grid_luta.addWidget(self.label,0,2)
        self.grid_luta.addWidget(self.btn_2,0,0)
        self.grid_luta.addWidget(self.btn_3,1,0)
        self.label.setText("Qual move irá utilizar?")

        self.btn_2.setText("Move1")
        self.btn.setText("Move2")
        self.btn_3.setText("Move3")
        
        ##botoes adicionais do grid luta
        self.btn_4 = QPushButton("Move 4")
        self.grid_luta.addWidget(self.btn_4,1,1)

        self.btn_5 = QPushButton("Voltar")
        self.grid_luta.addWidget(self.btn_5,1,2)
        self.btn_5.clicked.connect(self.menu)

        self.setLayout(self.grid_luta)
        
        
        


    def bag_btn(self):
        self.btn.hide()
        print("bag")

    def run_btn(self):
        self.grid.hide()
        print("run")
        

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec())
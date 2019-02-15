import sys
import requests
from PyQt5.QtWidgets import (QWidget, QLabel, QComboBox,
    QLineEdit, QApplication, QButtonGroup, QRadioButton,
    QVBoxLayout, QHBoxLayout)


class Window(QWidget):

    def __init__(self):
        super().__init__()
        
        self.getJSON()
        self.initUI()


    def getJSON(self):

        apiLink = "http://www.floatrates.com/daily/rub.json"
        resp = requests.get(url=apiLink)
        self.data = resp.json()
        
    def initUI(self):

        self.inputQLE = QLineEdit(self)
        self.inputQLE.move(80, 60)
        self.inputQLE.textChanged[str].connect(self.onInputChanged)

        self.labelRoubles = QLabel(self)
        self.labelRoubles.setText("Рубль")
        self.labelRoubles.move(300, 20)
        self.outputQLE = QLineEdit(self)
        self.outputQLE.move(300, 60)

        self.combo = QComboBox(self)
        self.combo.addItems(["Рубль", "Евро",
                        "Доллар", "Йена"])
        self.combo.move(80, 20)
        self.combo.activated[str].connect(self.onBoxActivated)

        self.nds10 = QRadioButton('10%')
        self.nds10.toggled.connect(self.onBoxActivated)
        self.nds18 = QRadioButton('18%')
        self.nds18.toggled.connect(self.onBoxActivated)
        self.nds20 = QRadioButton('20%')
        self.nds20.toggled.connect(self.onBoxActivated)

        self.radiobuttonsLayout = QVBoxLayout(self)
        self.radiobuttonsLayout.addWidget(QLabel("НДС"))       
        self.radiobuttonsLayout.addWidget(self.nds10)
        self.radiobuttonsLayout.addWidget(self.nds18)
        self.radiobuttonsLayout.addWidget(self.nds20)
        self.radiobuttonsLayout.addStretch()
        
        self.setGeometry(300, 300, 490, 270)
        self.setWindowTitle('QLineEdit')
        self.show()


    def onInputChanged(self, text):
        self.getOutput()

    def onBoxActivated(self, text):
        self.getOutput()

    def getOutput(self):

        #словарь валюты и ее кодов
        currencyCodesDict = {'Евро':'eur', 'Доллар':'usd', 'Йена':'jpy'}

        #курс рубля к разной валюте
        rate = 1
        if(str(self.combo.currentText()) != "Рубль"):
            rate = float(self.data[currencyCodesDict[str(
                self.combo.currentText())]]["inverseRate"])
        else:
            rate = 1

        #проверяем, есть ли что-то во входе           
        if(self.inputQLE.text() != ""):
            inputValue = float(self.inputQLE.text())
        else:
            inputValue = 0

        nds = 1
        
        if(self.nds10.isChecked()):
            nds = 1.1
        elif(self.nds18.isChecked()):
            nds = 1.18
        elif(self.nds20.isChecked()):
            nds = 1.2
            
        #вычисляем результат
        result = inputValue*rate*nds
        print(nds)
        self.outputQLE.setText(str(round(result, 2)))
        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

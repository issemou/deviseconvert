import py_currency_converter
from PySide6 import QtWidgets


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.setup_connections()
        self.set_default_values()
        self.setup_css()
        self.resize(500, 50)

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout(self)
        self.cbb_devisesFrom = QtWidgets.QComboBox()
        self.le_montant = QtWidgets.QSpinBox()
        self.cbb_devisesTo = QtWidgets.QComboBox()
        self.le_montantConverti = QtWidgets.QSpinBox()
        self.btn_inverser = QtWidgets.QPushButton("Inverser devises")

        self.layout.addWidget(self.cbb_devisesFrom)
        self.layout.addWidget(self.le_montant)
        self.layout.addWidget(self.cbb_devisesTo)
        self.layout.addWidget(self.le_montantConverti)
        self.layout.addWidget(self.btn_inverser)

    def setup_connections(self):
        self.cbb_devisesFrom.activated.connect(self.compute)
        self.cbb_devisesTo.activated.connect(self.compute)
        self.le_montant.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.inverser_devises)

    def setup_css(self):
        self.setStyleSheet("""
        background-color: rgb(30, 30, 30);
        color: rgb(240, 240, 240);
        border: none;
        """)
        style = """
        QComboBox::down-arrow {
            image: none;
            border-width: 0px;
        }
        QComboBox::drop-down {
            border-width: 0px;
        } 
        """
        self.cbb_devisesFrom.setStyleSheet(style)
        self.cbb_devisesTo.setStyleSheet(style)

    def set_default_values(self):
        self.cbb_devisesFrom.addItems(sorted(list()))
        self.cbb_devisesTo.addItems(sorted(list()))
        self.cbb_devisesFrom.setCurrentText("EUR")
        self.cbb_devisesTo.setCurrentText("EUR")
        self.le_montant.setValue(100)
        self.le_montantConverti.setValue(100)
        self.le_montant.setRange(1, 1000000)
        self.le_montantConverti.setRange(1, 1000000)

    def compute(self):
        montant = self.le_montant.value()
        deviseFrom = self.cbb_devisesFrom.currentText()
        deviseTo = self.cbb_devisesTo.currentText()

        try:
            resultat = self.py_currency_converter.convert(montant, deviseFrom, deviseTo)
        except py_currency_converter.convert().RateNotFoundError:
            print("Rate not found")
        else:
            self.le_montantConverti.setValue(resultat)

    def inverser_devises(self):
        devise_from = self.cbb_devisesFrom.currentText()
        devise_to = self.cbb_devisesTo.currentText()

        self.cbb_devisesFrom.setCurrentText(devise_to)
        self.cbb_devisesTo.setCurrentText(devise_from)
        self.compute()


app = QtWidgets.QApplication([])
win = App()
win.show()
app.exec_()

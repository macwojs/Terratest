"""
Glowna os programu z interfejsem
"""

import sys
import os
import terratest
from pygal import Line
import googlemap
from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QApplication, QLabel, QGridLayout,
                             QTextEdit, QStackedWidget, QWidget, QPushButton, QFileDialog,
                             QHBoxLayout, QDesktopWidget, QVBoxLayout)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import (QWebEngineView)

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        # Zmienna określająca który plik będzie teraz otwarty i zmienna ze ścieżką do pliku
        self.file_number = 0
        self.file_path = ""
        self.badanie = ""

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.maingui()

        self.mainwindow()

    # Wyświetlenie głównego gui programu
    def maingui(self):
        self.main_screen = MainScreen(self)
        self.central_widget.addWidget(self.main_screen)
        self.central_widget.setCurrentWidget(self.main_screen)

        if self.file_path:
            self.file_disp()
            self.main_screen.pathtext.setText(str(self.file_path[0][self.file_number]))

    # Wyświetlenie poprzeniengo pliku
    def clik_left(self):
        if not self.file_path:
            return

        if self.file_number == 0:
            self.file_number = (len(self.file_path[0]) - 1)
        else:
            self.file_number -= 1

        self.main_screen.textedit.clear()
        self.file_disp()
        self.main_screen.pathtext.setText(str(self.file_path[0][self.file_number]))

    # Wyświetlenie następnego pliku
    def clik_right(self):
        if not self.file_path:
            return

        if self.file_number == (len(self.file_path[0]) - 1):
            self.file_number = 0
        else:
            self.file_number += 1

        self.main_screen.textedit.clear()
        self.file_disp()
        self.main_screen.pathtext.setText(str(self.file_path[0][self.file_number]))

    # Funkcja wybierania pliku
    def selectfile(self):
        self.file_path = QFileDialog.getOpenFileNames(self, 'Open file',
                                                      '/home/PycharmProjects/Terratest/dane/',
                                                      "Terratest (*.TTD)")

        self.file_number = 0

        if self.file_path[1]:
            self.file_number = 0
            self.main_screen.textedit.clear()
            self.file_disp()
            self.main_screen.pathtext.setText(str(self.file_path[0][self.file_number]))
            self.statusBar().showMessage('Wybrano plik')

    # Wyświetlanie rozkodowanego pliku
    def file_disp(self):
        if self.file_path:
            self.badanie = terratest.Terratest(self.file_path[0][self.file_number])
            data = self.badanie.generete_report()
            self.main_screen.textedit.setText(data)
            self.plot_disp()

        self.statusBar().showMessage('Plik został rozkodowany')

    # Wyświetlanie wykresu
    def plot_disp(self):

        s1, s2, s3, x = self.badanie.plotdata()

        chart = Line()
        chart.x_title = 'Czas'
        chart.y_title = 'Ugięcie'
        # chart.title = 'Wykres ugięcia gruntu przy badaniu'
        chart.x_labels = map(str, x)
        chart.x_labels_major_count = 20
        chart.show_minor_x_labels = False
        chart.x_label_rotation = 60
        chart.add('Zrzut 1', s1)
        chart.add('Zrzut 2', s2)
        chart.add('Zrzut 3', s3)
        chart.render(is_unicode=True)
        plotpath = 'plots/plot.svg'
        chart.render_to_file(plotpath)
        ploturl = "file:///home/macwojs/PycharmProjects/Terratest/" + plotpath
        self.main_screen.plotview.load(QUrl(ploturl))

    # Czyszczenie wczytanych danych
    def clean(self):
        self.file_path = ''
        self.file_number = 0
        self.badanie = ''
        self.main_screen.pathtext.clear()
        self.main_screen.textedit.clear()

    # Wyświetlenie gui map
    def mapgui(self):
        if not self.file_path:
            return

        self.map_screen = MapScreen(self)

        latitude, longitude = self.badanie.coordinates_g()
        self.map_screen.drawmap(latitude, longitude)

        self.central_widget.addWidget(self.map_screen)
        self.central_widget.setCurrentWidget(self.map_screen)

        self.statusBar().showMessage('Wyświetlono mapę')

    # Deklaracja parametrów okna
    def mainwindow(self):
        self.statusBar().showMessage('Gotowy')
        self.resize(700, 600)
        self.center()
        self.setWindowTitle('Terratest')
        self.setWindowIcon(QIcon("img/icon.png"))
        self.show()

    # Centruje okno aplikacji
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


# Kod gównego gui
class MainScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pathtext = QLineEdit()
        pathlabel = QLabel("Podaj ścieżkę do pliku: ")
        self.pathbttn = QPushButton('...')
        pathgrid = QGridLayout()
        pathgrid.addWidget(pathlabel, 1, 0, 1, 4)
        pathgrid.addWidget(self.pathtext, 2, 0, 1, 1)
        pathgrid.addWidget(self.pathbttn, 2, 1, 1, 3)

        self.textedit = QTextEdit()
        self.plotview = QWebEngineView()
        datagrid = QGridLayout()
        datagrid.addWidget(self.textedit, 1, 0, 4, 5)
        datagrid.addWidget(self.plotview, 5, 0, 5, 5)

        self.bttnclean = QPushButton('Czyść dane')
        bttnpdf = QPushButton('Generuj PDF')
        self.bttnmap = QPushButton('Map')
        bttngrid = QGridLayout()
        bttngrid.addWidget(self.bttnclean, 1, 1, 1, 1)
        bttngrid.addWidget(bttnpdf, 1, 2, 1, 2)
        bttngrid.addWidget(self.bttnmap, 1, 4, 1, 2)

        self.grid = QGridLayout()
        self.grid.addLayout(pathgrid, 1, 0, 1, 1)
        self.grid.addLayout(datagrid, 2, 0, 12, 1)
        self.grid.addLayout(bttngrid, 14, 0, 1, 1)

        self.bttn2left = QPushButton('<')
        self.bttn2right = QPushButton('>')
        bttn2box = QHBoxLayout()
        bttn2box.addWidget(self.bttn2left)
        bttn2box.addStretch(1)
        bttn2box.addWidget(self.bttn2right)
        self.grid.addLayout(bttn2box, 15, 0, 1, 1)
        self.setLayout(self.grid)

        self.pathbttn.clicked.connect(self.parent().selectfile)
        self.bttnclean.clicked.connect(self.parent().clean)

        self.bttn2left.clicked.connect(self.parent().clik_left)
        self.bttn2right.clicked.connect(self.parent().clik_right)

        self.bttnmap.clicked.connect(self.parent().mapgui)


# Kod gui map
class MapScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backbttn = QPushButton("<--")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.backbttn)

        # Blok wyświetlający mapę z badaniem
        vbox = QVBoxLayout()
        curentpath = os.path.dirname(os.path.abspath(__file__))
        mapurl = 'file://'+curentpath+'/maps/mapa.html'
        self.mapview = QWebEngineView()
        self.mapview.load(QUrl(mapurl))
        vbox.addWidget(self.mapview)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.backbttn.clicked.connect(self.parent().maingui)

    def drawmap(self, lati, long):
        gmap = googlemap.GoogleMapPlotterKey(lati, long, 13)
        gmap.marker(lati, long, title="A street corner in Seattle")
        gmap.draw('maps/mapa.html')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())

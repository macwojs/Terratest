from gui import *
import sys
from PyQt5.QtWidgets import QApplication

#form interface import *
#from tkinter import *

#root = Tk()
#root.title("Terratest")
#root.geometry("500x400")
#app = Application(root)
#root.mainloop()

app = QApplication(sys.argv)
ex = Application()
sys.exit(app.exec_())
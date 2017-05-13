from tkinter import *
import terratest


class Application(Frame):
    """ GUI do aplikacji terratest """

    def __init__(self, master):
        """ Inicjalizuj ramkę. """
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """ Utwórz widżety do interfejsu"""
        # utwórz etykietę z instrukcją

        self.label_path= Label(self, text="Wprowadź ścieżkę do pliku")
        self.label_path.grid(row=0, column=0, columnspan=2, sticky=W)
        self.path = Entry(self)
        self.path.grid(row=0, column=2, columnspan=2, sticky=W)
        self.bttn_decode = Button(self, text="Dekoduj", command=self.reveal)
        self.bttn_decode.grid(row=1, column=0, sticky=W)
        self.report_txt = Text(self, width=35, height=5, wrap=WORD)
        self.report_txt.grid(row=3, column=0, columnspan=2, sticky=W)

    def reveal(self):
        """ Wyświetl raport"""

        file_path = self.path.get()
        test = terratest.Terratest(file_path)

        text = test.generete_report()

        self.report_txt.insert(0.0, text)
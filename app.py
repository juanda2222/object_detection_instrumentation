
import sys
from PySide2.QtWidgets import QApplication
from view import View
from model import Model
from controller import Controller


#custom qt widgets (chek box):    http://doc.qt.io/archives/qt-4.8/stylesheet-examples.html
#                                 https://doc.qt.io/archives/qq/qq20-qss.html
#                                 https://stackoverflow.com/questions/40672817/how-to-make-color-for-checked-qradiobutton-but-looks-like-standard
#                                 http://doc.qt.io/qt-5/stylesheet-examples.html


def main():

    app = QApplication(sys.argv)


    my_controller = Controller()
    my_view = View("./form.ui", my_controller)
    my_model = Model(my_controller)

    my_controller.add_view_model(my_view, my_model)  # for the bilateral comunication

    sys.exit(app.exec_())
    print("executed")

if __name__ == "__main__":
    main()

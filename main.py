#
#   ||||||||   || |||||| ||||||
#      ||      || ||  ||   ||
#      ||      || ||||||   ||
#   |||||   ||||| ||  ||   ||
# Author: Jaime Jjat 
# Date: Abril de 2019
# e-mail: userjjat00@gmail.com
# Youtube: https://www.youtube.com/channel/UC_SdV1G11_uYdfCDWrbLVWg/videos?view_as=subscriber
#
import sys
from PySide2.QtWidgets import QApplication
from view import View
from model import Model
from controller import Controller

def main():

    app = QApplication(sys.argv)

    my_controller = Controller()
    my_view = View("./form.ui", my_controller)
    my_model = Model(my_controller)

    my_controller.add_view_model(my_view, my_model)  # for the bilateral comunication

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()


#   _______________________________________________________________________________________
#  || - - - - - - - - - - - ||            |                                               ||
#  || - - ||||||||||||\ - - ||   AUTHOR:  |  Juan David Ramirez                           ||
#  || - - - ||| |||- ||| - -||____________|_______________________________________________||
#  || - - - ||| |||- ||| - -||            |                                               ||
#  || - - - ||| ||||||/ - - ||     DATE:  |  Abril de 2019                                ||
#  || - - - ||| - - - - - - ||____________|_______________________________________________||
#  || - - - ||| ||||||\ - - ||            |                                               ||
#  || - - - ||| |||- ||| - -||   E-MAIL:  |  juan.ramirez.villegas@correounivalle.edu.co  ||
#  || - - - ||| ||||||/ - - ||____________|_______________________________________________||
#  || - - -|||| |||- ||\ - -||                                                            ||
#  || -|||||| - - - - - - - ||               * * * * USE WISELY * * * *                   ||                                   
#  || - - - - - - - - - - - ||____________________________________________________________||                                                             
#  ****************************************************************************************

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
    print("executed")

if __name__ == "__main__":
    main()


class Controller():

    def __init__(self):
        self.controller = None
        self.view = None

    def add_view_model(self, view, controller):
        self.view = view
        self.controller = controller
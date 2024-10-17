from views.main_view import MainView
from controllers.beo_controller import BEOController
from models.beo_manager import BEOManager

def main():
    model = BEOManager()
    view = MainView()
    controller = BEOController(model, view)
    view.set_controller(controller)
    view.mainloop()

if __name__ == '__main__':
    main()

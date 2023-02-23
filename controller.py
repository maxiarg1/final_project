from tkinter import Tk
import view
import my_observer


class Controller:
    def __init__(self, root):
        self.root_controller = root
        self.objeto_vista = view.MyView(self.root_controller)
        self.el_observador = my_observer.ConcreteObserverA(self.objeto_vista.obj)

if __name__ == "__main__":
    root_tk = Tk()
    Controller(root_tk)
    root_tk.mainloop()

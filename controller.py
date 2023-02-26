from tkinter import Tk
import view
import my_server
import my_observer
import threading



class Controller:
    def __init__(self, root):
        self.root_controller = root
        self.objeto_vista = view.MyView(self.root_controller)
        self.el_observador = my_observer.ConcreteObserverA(self.objeto_vista.obj)

if __name__ == "__main__":
    root_tk = Tk()
    Controller(root_tk)
    server = my_server.Server()
    threading.Thread(target=server.start).start()
    print("Servidor en ejecución")
    root_tk.mainloop()

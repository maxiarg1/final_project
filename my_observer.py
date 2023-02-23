class Subject:

    observers = []

    def agregar(self, obj):
        self.observers.append(obj)

    def quitar(self, obj):
        pass

    def notificar(self, *args):
        for observer in self.observers:
            observer.update(args)


class Observer:
    def update(self):
        raise NotImplementedError("Delegación de actualización")


class ConcreteObserverA(Observer):
    def __init__(self, obj):
        self.observado_a = obj
        self.observado_a.agregar(self)

    def update(self, *args):
        print("Actualización dentro de ObservadorConcretoA")
        print("Aquí están los parámetros: ", args)

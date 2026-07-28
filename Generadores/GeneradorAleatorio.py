from abc import ABC, abstractmethod

class GeneradorAleatorio(ABC):

    @abstractmethod
    def generar_numero_aleatorio(self, cantidad_a_generar: int) -> list[float]:
        pass
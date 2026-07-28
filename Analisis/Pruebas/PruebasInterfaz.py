from abc import ABC, abstractmethod
from typing import Any


class PruebaInterfaz(ABC):
    @abstractmethod
    def ejecutar(self, numeros: list[float]) -> Any:
        pass
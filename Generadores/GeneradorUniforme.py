import numpy as np

class GeneradorUniforme:
    
    @staticmethod
    def generar_continua(cantidad: int, minimo: float = 0.0, maximo: float = 1.0) -> list[float]:
        """Genera números aleatorios bajo una distribución uniforme continua U(min, max)."""
        return np.random.uniform(minimo, maximo, cantidad).tolist()

    @staticmethod
    def generar_discreta(cantidad: int, minimo: int = 1, maximo: int = 10) -> list[int]:
        """Genera números enteros aleatorios bajo una distribución uniforme discreta."""
        return np.random.randint(minimo, maximo + 1, cantidad).tolist()
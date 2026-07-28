from Generadores.GeneradorAleatorio import GeneradorAleatorio
from Dto.AuditoriaDto import CongruencialDto


class GeneradorCongruencial(GeneradorAleatorio):

    def __init__(self, valores: CongruencialDto):
        # Guardamos la configuración inmutable
        self._valor = valores

    def generar_numero_aleatorio(self, cantidad_a_generar: int) -> list[float]:
        lista_numeros_aleatorios: list[float] = []
        estado_actual: int = self._valor.semilla

        for _ in range(cantidad_a_generar):
            siguiente_estado: int = (
            self._valor.multiplicador * estado_actual + self._valor.incremento
            ) % self._valor.modulo

            numero_uniforme: float = siguiente_estado / max(1, self._valor.modulo)
            lista_numeros_aleatorios.append(numero_uniforme)
            estado_actual = siguiente_estado

        return lista_numeros_aleatorios
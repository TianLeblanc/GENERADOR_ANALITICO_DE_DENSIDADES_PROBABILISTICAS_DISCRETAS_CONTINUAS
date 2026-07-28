import math
from scipy.stats import norm
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO


class PruebaMedia(PruebaInterfaz):

    def __init__(self, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de la Media"
        self._nivel_confianza = nivel_confianza
        
        # CÁLCULO DINÁMICO DE Z CRÍTICO (Distribución Normal Estándar)
        # Bilateral: Alfa se divide en dos colas (alfa / 2)
        alfa = 1.0 - nivel_confianza
        self._z_critico = round(norm.ppf(1.0 - alfa / 2.0), 4)

    def ejecutar(self, numeros: list[float]) -> ResultadoPruebaDTO:
        n = len(numeros)

        if n == 0:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=self._z_critico,
                pasa_validacion=False
            )

        media_muestra = sum(numeros) / n
        desviacion_teorica = 1 / math.sqrt(12 * n)
        valor_z = (media_muestra - 0.5) / desviacion_teorica

        pasa_validacion = abs(valor_z) < self._z_critico

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(valor_z, 4),
            valor_critico_tabla=self._z_critico,
            valor_crudo=round(media_muestra,4),
            pasa_validacion=pasa_validacion
        )
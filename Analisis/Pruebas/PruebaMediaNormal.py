import math
from scipy.stats import norm
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO


class PruebaMediaNormal(PruebaInterfaz):

    def __init__(self, media_teorica: float, desv_teorica: float, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de la Media (Normal)"
        self._media_teorica = media_teorica
        self._desv_teorica = desv_teorica
        self._nivel_confianza = nivel_confianza

        alfa = 1.0 - nivel_confianza
        self._z_critico = round(norm.ppf(1.0 - alfa / 2.0), 4)

    def ejecutar(self, numeros: list[float]) -> ResultadoPruebaDTO:
        n = len(numeros)

        if n == 0:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=round(self._z_critico),
                pasa_validacion=False
            )

        media_muestra = sum(numeros) / n
        # Desviación estándar del error estándar para la media normal: sigma / sqrt(n)
        error_estandar = self._desv_teorica / math.sqrt(n)

        if error_estandar == 0:
            valor_z = 0.0 if media_muestra == self._media_teorica else float('inf')
        else:
            valor_z = (media_muestra - self._media_teorica) / error_estandar

        pasa_validacion = abs(valor_z) < self._z_critico

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(valor_z, 4),
            valor_critico_tabla=round(self._z_critico),
            valor_crudo=round(media_muestra, 4),
            pasa_validacion=pasa_validacion
        )
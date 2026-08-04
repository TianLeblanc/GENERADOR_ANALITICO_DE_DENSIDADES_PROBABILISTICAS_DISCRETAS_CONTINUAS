import math
from scipy.stats import norm
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO

class PruebaMediaDiscreta(PruebaInterfaz):
    def __init__(self, min_val: int, max_val: int, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de la Media (Uniforme Discreta)"
        self._min_val = min_val
        self._max_val = max_val
        self._nivel_confianza = nivel_confianza
        
        self._media_teorica = (min_val + max_val) / 2.0
        
        alfa = 1.0 - nivel_confianza
        self._z_critico = round(norm.ppf(1.0 - alfa / 2.0), 4)

    def ejecutar(self, numeros: list[float]) -> ResultadoPruebaDTO:
        # Convertimos forzosamente a enteros para evitar desajustes en las sumatorias
        nums_enteros = [int(x) for x in numeros]
        n = len(nums_enteros)
        
        if n == 0:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=self._z_critico,
                pasa_validacion=False
            )

        media_muestra = sum(nums_enteros) / n
        
        a, b = self._min_val, self._max_val
        varianza_teorica = (((b - a + 1) ** 2) - 1) / 12.0
        error_estandar = math.sqrt(varianza_teorica / n)

        if error_estandar == 0:
            valor_z = 0.0 if media_muestra == self._media_teorica else float('inf')
        else:
            valor_z = (media_muestra - self._media_teorica) / error_estandar

        pasa_validacion = abs(valor_z) <= self._z_critico

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(valor_z, 4),
            valor_critico_tabla=self._z_critico,
            pasa_validacion=pasa_validacion
        )
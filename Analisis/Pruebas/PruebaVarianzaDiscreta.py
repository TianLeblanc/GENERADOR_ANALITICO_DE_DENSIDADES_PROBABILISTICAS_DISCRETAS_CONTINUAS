from scipy.stats import chi2
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO

class PruebaVarianzaDiscreta(PruebaInterfaz):
    def __init__(self, min_val: int, max_val: int, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de la Varianza (Uniforme Discreta)"
        self._nivel_confianza = nivel_confianza
        
        a, b = min_val, max_val
        self._varianza_teorica = (((b - a + 1) ** 2) - 1) / 12.0

    def ejecutar(self, numeros: list[float]) -> ResultadoPruebaDTO:
        # Convertimos forzosamente a enteros
        nums_enteros = [int(x) for x in numeros]
        n = len(nums_enteros)
        
        if n <= 1 or self._varianza_teorica <= 0:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=0.0,
                pasa_validacion=False
            )

        media = sum(nums_enteros) / n
        suma_cuadrados = sum((x - media) ** 2 for x in nums_enteros)
        varianza_muestra = suma_cuadrados / (n - 1)

        estadistico_chi = ((n - 1) * varianza_muestra) / self._varianza_teorica

        gl = n - 1
        alfa = 1.0 - self._nivel_confianza
        chi_inferior = chi2.ppf(alfa / 2.0, df=gl)
        chi_superior = chi2.ppf(1.0 - alfa / 2.0, df=gl)

        pasa_validacion = chi_inferior <= estadistico_chi <= chi_superior

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(estadistico_chi, 4),
            valor_critico_tabla=round(chi_superior, 4),
            pasa_validacion=pasa_validacion
        )
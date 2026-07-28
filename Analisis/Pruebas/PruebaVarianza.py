import math
from scipy.stats import chi2
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO


class PruebaVarianza(PruebaInterfaz):

    def __init__(self, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de la Varianza"
        self._nivel_confianza = nivel_confianza
        self._varianza_teorica = 1 / 12

    def ejecutar(self, numeros: list[float]) -> ResultadoPruebaDTO:
        n = len(numeros)

        if n <= 1:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=0.0,
                pasa_validacion=False
            )

        # 1. Calcular la media y varianza real de los datos
        media = sum(numeros) / n
        suma_cuadrados = sum((x - media) ** 2 for x in numeros)
        varianza_muestra = suma_cuadrados / (n - 1)

        # 2. Calcular el estadístico de prueba Chi-cuadrado
        estadistico_chi = ((n - 1) * varianza_muestra) / self._varianza_teorica

        # 3. CÁLCULO DINÁMICO DE LÍMITES CRÍTICOS (Distribución Chi-Cuadrado)
        gl = n - 1
        alfa = 1.0 - self._nivel_confianza
        
        chi_inferior = chi2.ppf(alfa / 2.0, df=gl)
        chi_superior = chi2.ppf(1.0 - alfa / 2.0, df=gl)

        # 4. Validar si cae en la zona de aceptación
        pasa_validacion = chi_inferior <= estadistico_chi <= chi_superior

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(estadistico_chi, 4),
            # Enviamos ambos límites formateados como referencia visual clara
            valor_critico_tabla=f"[{round(chi_inferior, 2)}, {round(chi_superior, 2)}]",
            pasa_validacion=pasa_validacion
        )
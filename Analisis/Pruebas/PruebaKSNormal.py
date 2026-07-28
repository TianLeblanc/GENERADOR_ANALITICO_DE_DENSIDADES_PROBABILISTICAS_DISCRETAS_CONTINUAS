import math
from scipy.stats import norm, kstwobign
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO, DatosGraficaKSDTO


class PruebaKSNormal(PruebaInterfaz):

    def __init__(self, media_teorica: float, desv_teorica: float, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de Kolmogorov-Smirnov (Normal)"
        self._media_teorica = media_teorica
        self._desv_teorica = desv_teorica
        self._nivel_confianza = nivel_confianza
        self.ultimos_datos_grafica: DatosGraficaKSDTO | None = None

    def ejecutar(self, numeros: list[float]) -> ResultadoPruebaDTO:
        n = len(numeros)

        if n == 0:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=0.0,
                pasa_validacion=False
            )

        numeros_ordenados = sorted(numeros)

        prob_teorica = []
        prob_real = []
        d_max = 0.0

        for i in range(1, n + 1):
            x_i = numeros_ordenados[i - 1]

            # Probabilidad acumulada teórica según la distribución normal F_0(x_i)
            F_teorica = norm.cdf(x_i, loc=self._media_teorica, scale=self._desv_teorica)

            # Probabilidades empíricas de la escalera
            altura_real_superior = i / n
            altura_real_inferior = (i - 1) / n

            prob_teorica.append(F_teorica)
            prob_real.append(altura_real_superior)

            d_mas = abs(altura_real_superior - F_teorica)
            d_menos = abs(F_teorica - altura_real_inferior)

            d_max = max(d_max, d_mas, d_menos)

        alfa = 1.0 - self._nivel_confianza
        coeficiente_ks = kstwobign.ppf(1.0 - alfa)
        valor_critico = coeficiente_ks / math.sqrt(n)

        # Memento para la gráfica CDF en la UI
        self.ultimos_datos_grafica = DatosGraficaKSDTO(
            numeros_ordenados=numeros_ordenados,
            probabilidad_teorica=prob_teorica,
            probabilidad_real=prob_real
        )

        pasa_validacion = d_max < valor_critico

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(d_max, 4),
            valor_critico_tabla=round(valor_critico, 4),
            pasa_validacion=pasa_validacion
        )
import math
from scipy.stats import kstwobign
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO, DatosGraficaKSDTO


class PruebaKS(PruebaInterfaz):

    def __init__(self, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de Kolmogorov-Smirnov"
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

        # Si los números son enteros o están fuera de [0, 1], los normalizamos para K-S de manera segura
        min_v, max_v = min(numeros), max(numeros)
        if max_v > 1.0 or min_v < 0.0:
            rango = max_v - min_v
            if rango == 0:
                rango = 1.0
            datos_proc = [(x - min_v) / rango for x in numeros]
        else:
            datos_proc = list(numeros)

        numeros_ordenados = sorted(datos_proc)

        prob_teorica = []
        prob_real = []
        d_max = 0.0

        for i in range(1, n + 1):
            x_i = numeros_ordenados[i - 1]
            altura_teorica = i / n

            prob_teorica.append(x_i)
            prob_real.append(altura_teorica)

            d_mas = altura_teorica - x_i
            d_menos = x_i - ((i - 1) / n)
            d_max = max(d_max, d_mas, d_menos)

        alfa = 1.0 - self._nivel_confianza
        coeficiente_ks = kstwobign.ppf(1.0 - alfa)
        valor_critico = coeficiente_ks / math.sqrt(n)

        self.ultimos_datos_grafica = DatosGraficaKSDTO(
            numeros_ordenados=numeros_ordenados,
            probabilidad_teorica=numeros_ordenados,
            probabilidad_real=prob_real
        )

        pasa_validacion = d_max < valor_critico

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(d_max, 4),
            valor_critico_tabla=round(valor_critico, 4),
            pasa_validacion=pasa_validacion
        )
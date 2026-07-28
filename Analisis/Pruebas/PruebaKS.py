import math
from scipy.stats import kstwobign
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO, DatosGraficaKSDTO


class PruebaKS(PruebaInterfaz):

    def __init__(self, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de Kolmogorov-Smirnov"
        self._nivel_confianza = nivel_confianza
        # Propiedad interna para almacenar los datos de la gráfica tras ejecutar
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

        # 1. El corazón de KS: Ordenar los datos de menor a mayor
        numeros_ordenados = sorted(numeros)

        # 2. Inicializar vectores para la futura gráfica y cálculo de distancias
        prob_teorica = []
        prob_real = []
        d_max = 0.0

        # 3. Bucle analítico para calcular distancias D+ y D-
        for i in range(1, n + 1):
            x_i = numeros_ordenados[i - 1]

            # Altura de la escalera en este paso
            altura_teorica = i / n

            # Guardamos los puntos para la UI gráfica
            prob_teorica.append(x_i)  # En un mundo ideal, X_i debería ser igual a i/n
            prob_real.append(altura_teorica)

            # Distancias estadísticas
            d_mas = altura_teorica - x_i
            d_menos = x_i - ((i - 1) / n)

            # Nos quedamos con el peor caso (la distancia más larga)
            d_max = max(d_max, d_mas, d_menos)

        # 4. CÁLCULO DINÁMICO DEL VALOR CRÍTICO DE K-S
        # Reemplazamos el coeficiente fijo (1.36) calculando el percentil exacto 
        # de la distribución limite de Kolmogorov (kstwobign) según el nivel de confianza.
        alfa = 1.0 - self._nivel_confianza
        coeficiente_ks = kstwobign.ppf(1.0 - alfa)
        valor_critico = coeficiente_ks / math.sqrt(n)

        # 5. Guardar el Memento visual para la interfaz gráfica
        self.ultimos_datos_grafica = DatosGraficaKSDTO(
            numeros_ordenados=numeros_ordenados,
            probabilidad_teorica=numeros_ordenados,  # La diagonal Y = X
            probabilidad_real=prob_real
        )

        pasa_validacion = d_max < valor_critico

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(d_max, 4),
            valor_critico_tabla=round(valor_critico, 4),
            pasa_validacion=pasa_validacion
        )
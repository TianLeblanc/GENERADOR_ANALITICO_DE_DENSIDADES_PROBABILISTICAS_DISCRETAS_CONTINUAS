from scipy.stats import chi2
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO, DatosGraficaKSDTO

class PruebaChiCuadrada(PruebaInterfaz):
    def __init__(self, min_d: int, max_d: int, nivel_confianza: float = 0.95):
        self._nombre = "Prueba Chi-cuadrada (Bondad de Ajuste)"
        self._min_d = min_d
        self._max_d = max_d
        self._nivel_confianza = nivel_confianza
        self.ultimos_datos_grafica: DatosGraficaKSDTO | None = None

    def ejecutar(self, numeros: list[float]) -> ResultadoPruebaDTO:
        n = len(numeros)
        valores_posibles = list(range(int(self._min_d), int(self._max_d) + 1))
        k = len(valores_posibles)

        if n == 0 or k == 0:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=0.0,
                pasa_validacion=False
            )

        # Frecuencia esperada teórica para cada valor en Uniforme Discreta
        frecuencia_esperada = n / k

        # Conteo de frecuencias observadas en la muestra
        conteo_observado = {val: 0 for val in valores_posibles}
        for x in numeros:
            val_entero = int(round(x))
            if val_entero in conteo_observado:
                conteo_observado[val_entero] += 1

        # Cálculo del estadístico Chi-cuadrada: Suma de (O - E)^2 / E
        chi2_calculado = 0.0
        for val in valores_posibles:
            f_obs = conteo_observado[val]
            chi2_calculado += ((f_obs - frecuencia_esperada) ** 2) / frecuencia_esperada

        # Grados de libertad (k - 1)
        gl = k - 1
        alfa = 1.0 - self._nivel_confianza
        chi2_critico = chi2.ppf(1.0 - alfa, df=gl)

        pasa_validacion = chi2_calculado <= chi2_critico

        # Guardamos datos vacíos de K-S para que la gráfica no rompa la estructura
        self.ultimos_datos_grafica = DatosGraficaKSDTO(
            numeros_ordenados=[],
            probabilidad_teorica=[],
            probabilidad_real=[]
        )

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(chi2_calculado, 4),
            valor_critico_tabla=round(chi2_critico, 4),
            pasa_validacion=pasa_validacion
        )
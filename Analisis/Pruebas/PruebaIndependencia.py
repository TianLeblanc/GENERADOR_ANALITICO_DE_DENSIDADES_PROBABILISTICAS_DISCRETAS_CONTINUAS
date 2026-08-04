import math
from scipy.stats import norm
from Analisis.Pruebas.PruebasInterfaz import PruebaInterfaz
from Dto.AuditoriaDto import ResultadoPruebaDTO


class PruebaIndependencia(PruebaInterfaz):

    def __init__(self, nivel_confianza: float = 0.95):
        self._nombre = "Prueba de Independencia (Rachas)"
        self._nivel_confianza = nivel_confianza
        
        alfa = 1.0 - nivel_confianza
        self._z_critico = round(norm.ppf(1.0 - alfa / 2.0), 4)

    def ejecutar(self, numeros: list[float]) -> ResultadoPruebaDTO:
        n = len(numeros)

        if n < 2:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=self._z_critico,
                pasa_validacion=False
            )

        # Usamos la mediana de los datos como umbral dinámico para evitar que todos caigan del mismo lado
        temp_sort = sorted(numeros)
        mediana = temp_sort[n // 2]

        # 1. Secuencia de binarios basados en la mediana
        signos = [x >= mediana for x in numeros]

        # 2. Contar rachas (b)
        rachas = 1
        for i in range(1, n):
            if signos[i] != signos[i - 1]:
                rachas += 1

        # 3. Contar arriba (n1) y abajo (n2)
        n1 = sum(1 for s in signos if s)
        n2 = n - n1

        if n1 == 0 or n2 == 0:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=self._z_critico,
                pasa_validacion=False
            )

        # 4. Media y varianza teórica de las rachas
        media_rachas = ((2 * n1 * n2) / n) + 0.5
        numerador_var = 2 * n1 * n2 * (2 * n1 * n2 - n)
        denominador_var = (n ** 2) * (n - 1)
        
        if denominador_var == 0:
            varianza_rachas = 0.0
        else:
            varianza_rachas = numerador_var / denominador_var

        if varianza_rachas <= 0:
            return ResultadoPruebaDTO(
                nombre_prueba=self._nombre,
                valor_calculado=0.0,
                valor_critico_tabla=self._z_critico,
                pasa_validacion=False
            )

        # 5. Calcular estadístico Z_0
        valor_z = (rachas - media_rachas) / math.sqrt(varianza_rachas)

        # 6. Validar hipótesis bilateral
        pasa_validacion = abs(valor_z) < self._z_critico

        return ResultadoPruebaDTO(
            nombre_prueba=self._nombre,
            valor_calculado=round(valor_z, 4),
            valor_critico_tabla=self._z_critico,
            pasa_validacion=pasa_validacion
        )
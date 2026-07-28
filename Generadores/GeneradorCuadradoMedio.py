from Generadores.GeneradorAleatorio import GeneradorAleatorio


class GeneradorCuadradoMedio(GeneradorAleatorio):
    def __init__(self, semilla: int):
        self._semilla: int = semilla
        self._digitos_totales: int = len(str(semilla))

    def _extraer_centro_txt(self, numero_cuadrado: int) -> str:
        cadena_rellenada: str = str(numero_cuadrado).zfill(2 * self._digitos_totales)

        indice_inicio: int = (len(cadena_rellenada) - self._digitos_totales) // 2
        indice_fin: int = indice_inicio + self._digitos_totales

        return cadena_rellenada[indice_inicio:indice_fin]

    def generar_numero_aleatorio(self, cantidad_a_generar: int) -> list[float]:
        lista_numeros_aleatorios: list[float] = []
        estado_actual: int = self._semilla

        for _ in range(cantidad_a_generar):
            resultado_cuadrado: int = estado_actual ** 2

            digitos_centro_txt: str = self._extraer_centro_txt(resultado_cuadrado)

            estado_actual = int(digitos_centro_txt)

            numero_uniforme: float = float(f"0.{digitos_centro_txt}")
            lista_numeros_aleatorios.append(numero_uniforme)

            if estado_actual == 0:
                elementos_restantes: int = cantidad_a_generar - len(lista_numeros_aleatorios)
                lista_numeros_aleatorios.extend([0.0] * elementos_restantes)
                break

        return lista_numeros_aleatorios
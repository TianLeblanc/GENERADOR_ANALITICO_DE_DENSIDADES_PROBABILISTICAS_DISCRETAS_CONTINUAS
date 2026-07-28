from Dto.AuditoriaDto import ReporteAuditoriaDTO, MetadatosGeneradorDTO, DatosGraficaKSDTO
from Analisis.Pruebas.PruebaMedia import PruebaMedia
from Analisis.Pruebas.PruebaVarianza import PruebaVarianza
from Analisis.Pruebas.PruebaKS import PruebaKS
from Analisis.Pruebas.PruebaIndependencia import PruebaIndependencia


class AnalizadorEstadistico:

    def __init__(self, nivel_confianza: float = 0.95):
        self._nivel_confianza = nivel_confianza

        self._prueba_media = PruebaMedia(nivel_confianza)
        self._prueba_varianza = PruebaVarianza(nivel_confianza)
        self._prueba_ks = PruebaKS(nivel_confianza)
        self._prueba_independencia = PruebaIndependencia(nivel_confianza)

    def evaluar_generador(self, numeros: list[float], nombre_generador: str, parametros: dict) -> ReporteAuditoriaDTO:
        metadatos = MetadatosGeneradorDTO(
            nombre_generador=nombre_generador,
            parametros=parametros
        )

        # 2. Ejecutar cada una de las matemáticas en bloque
        res_media = self._prueba_media.ejecutar(numeros)
        res_varianza = self._prueba_varianza.ejecutar(numeros)
        res_ks = self._prueba_ks.ejecutar(numeros)
        res_independencia = self._prueba_independencia.ejecutar(numeros)

        # 3. Extraer el memento visual con un salvavidas para el linter de PyCharm
        datos_visuales = self._prueba_ks.ultimos_datos_grafica
        if datos_visuales is None:
            datos_visuales = DatosGraficaKSDTO(
                numeros_ordenados=[],
                probabilidad_teorica=[],
                probabilidad_real=[]
            )

        # 4. Construir y regresar la foto fija del experimento completo
        return ReporteAuditoriaDTO(
            metadatos=metadatos,
            numeros_generados=numeros,
            prueba_media=res_media,
            prueba_varianza=res_varianza,
            prueba_ks=res_ks,
            datos_visuales_ks=datos_visuales,
            prueba_independencia=res_independencia
        )
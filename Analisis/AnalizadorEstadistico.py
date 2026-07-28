from Dto.AuditoriaDto import ReporteAuditoriaDTO, MetadatosGeneradorDTO, DatosGraficaKSDTO
from Analisis.Pruebas.PruebaMedia import PruebaMedia
from Analisis.Pruebas.PruebaVarianza import PruebaVarianza
from Analisis.Pruebas.PruebaKS import PruebaKS
from Analisis.Pruebas.PruebaIndependencia import PruebaIndependencia

# Importamos las nuevas pruebas normales
from Analisis.Pruebas.PruebaMediaNormal import PruebaMediaNormal
from Analisis.Pruebas.PruebaVarianzaNormal import PruebaVarianzaNormal
from Analisis.Pruebas.PruebaKSNormal import PruebaKSNormal


class AnalizadorEstadistico:

    def __init__(self, nivel_confianza: float = 0.95, es_normal: bool = False, media: float = 0.0, desviacion: float = 1.0):
        self._nivel_confianza = nivel_confianza
        self._es_normal = es_normal

        if self._es_normal:
            # Si es normal, usamos las pruebas con los parámetros teóricos μ y σ
            self._prueba_media = PruebaMediaNormal(media, desviacion, nivel_confianza)
            self._prueba_varianza = PruebaVarianzaNormal(desviacion, nivel_confianza)
            self._prueba_ks = PruebaKSNormal(media, desviacion, nivel_confianza)
        else:
            # Si es uniforme por defecto [0, 1]
            self._prueba_media = PruebaMedia(nivel_confianza)
            self._prueba_varianza = PruebaVarianza(nivel_confianza)
            self._prueba_ks = PruebaKS(nivel_confianza)

        # La prueba de rachas/independencia se mantiene para evaluar la secuencia
        self._prueba_independencia = PruebaIndependencia(nivel_confianza)

    def evaluar_generador(self, numeros: list[float], nombre_generador: str, parametros: dict) -> ReporteAuditoriaDTO:
        metadatos = MetadatosGeneradorDTO(
            nombre_generador=nombre_generador,
            parametros=parametros
        )

        # 2. Ejecutar cada una de las pruebas matemáticas
        res_media = self._prueba_media.ejecutar(numeros)
        res_varianza = self._prueba_varianza.ejecutar(numeros)
        res_ks = self._prueba_ks.ejecutar(numeros)
        res_independencia = self._prueba_independencia.ejecutar(numeros)

        # 3. Extraer el memento visual para la gráfica K-S
        datos_visuales = self._prueba_ks.ultimos_datos_grafica
        if datos_visuales is None:
            datos_visuales = DatosGraficaKSDTO(
                numeros_ordenados=[],
                probabilidad_teorica=[],
                probabilidad_real=[]
            )

        # 4. Construir y regresar el reporte completo
        return ReporteAuditoriaDTO(
            metadatos=metadatos,
            numeros_generados=numeros,
            prueba_media=res_media,
            prueba_varianza=res_varianza,
            prueba_ks=res_ks,
            datos_visuales_ks=datos_visuales,
            prueba_independencia=res_independencia
        )
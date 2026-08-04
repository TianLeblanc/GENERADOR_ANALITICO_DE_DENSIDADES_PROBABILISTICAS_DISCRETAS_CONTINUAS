from Dto.AuditoriaDto import ReporteAuditoriaDTO, MetadatosGeneradorDTO, DatosGraficaKSDTO
from Analisis.Pruebas.PruebaChiCuadrada import PruebaChiCuadrada
from Analisis.Pruebas.PruebaIndependencia import PruebaIndependencia
from Analisis.Pruebas.PruebaMediaDiscreta import PruebaMediaDiscreta
from Analisis.Pruebas.PruebaVarianzaDiscreta import PruebaVarianzaDiscreta

class AnalizadorEstadistico:

    def __init__(self, nivel_confianza: float = 0.95, min_d: int = 1, max_d: int = 10, **kwargs):
        self._nivel_confianza = nivel_confianza
        self._min_d = min_d
        self._max_d = max_d
        
        # Pruebas estadísticas discretas oficiales
        self._prueba_media = PruebaMediaDiscreta(min_d, max_d, nivel_confianza)
        self._prueba_varianza = PruebaVarianzaDiscreta(min_d, max_d, nivel_confianza)
        self._prueba_chi = PruebaChiCuadrada(min_d, max_d, nivel_confianza)
        self._prueba_independencia = PruebaIndependencia(nivel_confianza)

    def evaluar_generador(self, numeros: list[float], nombre_generador: str, parametros: dict) -> ReporteAuditoriaDTO:
        metadatos = MetadatosGeneradorDTO(
            nombre_generador=nombre_generador,
            parametros=parametros
        )

        # Ejecución de pruebas con los valores enteros originales
        res_media = self._prueba_media.ejecutar(numeros)
        res_varianza = self._prueba_varianza.ejecutar(numeros)
        res_chi = self._prueba_chi.ejecutar(numeros)

        # Normalización para la prueba de rachas (independencia)
        rango = self._max_d - self._min_d
        if rango == 0:
            rango = 1.0
        numeros_normalizados = [min(max((x - self._min_d) / (rango + 1.0), 0.0), 0.999999) for x in numeros]
        res_independencia = self._prueba_independencia.ejecutar(numeros_normalizados)

        datos_visuales = DatosGraficaKSDTO(
            numeros_ordenados=[],
            probabilidad_teorica=[],
            probabilidad_real=[]
        )

        return ReporteAuditoriaDTO(
            metadatos=metadatos,
            numeros_generados=numeros,
            resultado_media=res_media,
            resultado_varianza=res_varianza,
            resultado_ks=res_chi,  # Reemplazamos K-S por Chi-cuadrada en el reporte estándar
            resultado_independencia=res_independencia,
            visuales_ks=datos_visuales
        )
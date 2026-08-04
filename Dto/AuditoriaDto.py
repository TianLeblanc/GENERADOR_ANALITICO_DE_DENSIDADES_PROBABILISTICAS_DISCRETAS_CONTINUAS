class ResultadoPruebaDTO:
    def __init__(self, nombre_prueba="", valor_calculado=0.0, valor_critico_tabla=0.0, pasa_validacion=False, detalles="", **kwargs):
        self.nombre_prueba = nombre_prueba
        self.valor_calculado = valor_calculado
        self.valor_critico_tabla = valor_critico_tabla
        self.pasa_validacion = pasa_validacion
        self.detalles = detalles

class MetadatosGeneradorDTO:
    def __init__(self, nombre_generador="", parametros=None, **kwargs):
        self.nombre_generador = nombre_generador
        self.parametros = parametros if parametros is not None else {}

class DatosGraficaKSDTO:
    def __init__(self, numeros_ordenados=None, probabilidad_teorica=None, probabilidad_real=None, **kwargs):
        self.numeros_ordenados = numeros_ordenados if numeros_ordenados is not None else []
        self.probabilidad_teorica = probabilidad_teorica if probabilidad_teorica is not None else []
        self.probabilidad_real = probabilidad_real if probabilidad_real is not None else []

class ReporteAuditoriaDTO:
    def __init__(self, metadatos=None, numeros_generados=None, resultado_media=None, resultado_varianza=None, resultado_ks=None, resultado_independencia=None, visuales_ks=None, **kwargs):
        self.metadatos = metadatos
        self.numeros_generados = numeros_generados if numeros_generados is not None else []
        self.resultado_media = resultado_media
        self.resultado_varianza = resultado_varianza
        self.resultado_ks = resultado_ks
        self.resultado_independencia = resultado_independencia
        self.visuales_ks = visuales_ks
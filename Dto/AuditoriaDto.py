from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class CongruencialDto:
    semilla: int
    multiplicador: int
    incremento: int
    modulo: int

@dataclass(frozen=True)
class ResultadoPruebaDTO:
    nombre_prueba: str
    valor_calculado: float
    valor_critico_tabla: float | str
    pasa_validacion: bool
    valor_crudo: float | None = None

@dataclass(frozen=True)
class DatosGraficaKSDTO:
    """Contiene las series de datos listas para que la UI dibuje la gráfica CDF sin calcular nada."""
    numeros_ordenados: list[float]
    probabilidad_teorica: list[float]
    probabilidad_real: list[float]

@dataclass(frozen=True)
class MetadatosGeneradorDTO:
    """Guarda el pasaporte del reporte: qué algoritmo lo creó y con qué variables."""
    nombre_generador: str
    parametros: dict[str, Any]

@dataclass(frozen=True)
class ReporteAuditoriaDTO:
    metadatos: MetadatosGeneradorDTO
    numeros_generados: list[float]
    prueba_media: ResultadoPruebaDTO
    prueba_varianza: ResultadoPruebaDTO
    prueba_ks: ResultadoPruebaDTO
    datos_visuales_ks: DatosGraficaKSDTO
    prueba_independencia: ResultadoPruebaDTO
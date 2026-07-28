# Analizador Estadístico de Generadores Pseudoaleatorios

Aplicación web desarrollada en **Streamlit** y Python para la generación estocástica de números aleatorios y su respectiva validación analítica mediante pruebas estadísticas rigurosas.

---

## 🚀 Características Principales

* **Generación de Distribuciones:** Soporte para distribuciones uniformes continuas (estándar $U(0,1)$ y personalizadas con límites $a$ y $b$) y uniformes discretas.
* **Pruebas Estadísticas Automatizadas:**
  * **Prueba de la Media:** Validación bilateral basada en la distribución normal estándar ($Z$).
  * **Prueba de la Varianza:** Validación mediante la distribución Chi-cuadrada ($\chi^2$).
  * **Prueba de Kolmogorov-Smirnov (K-S):** Evaluación de bondad de ajuste con cálculo dinámico del valor crítico límite.
  * **Prueba de Independencia (Rachas):** Análisis de aleatoriedad en el orden de secuencia.
* **Panel Visual (Dashboard):** Tarjetas de métricas estandarizadas con altura fija y gráficas analíticas interactivas.
* **Puente de Normalización Matemático:** Adaptación interna al rango $[0,1)$ para garantizar la validez de las pruebas estadísticas en cualquier rango personalizado, mostrando métricas reales desnormalizadas al usuario.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.x**
* **Streamlit** (Interfaz web)
* **SciPy / NumPy** (Cálculos estadísticos y distribuciones de probabilidad)

---

## 📦 Guía de Instalación y Configuración

Sigue estos pasos para clonar y poner en marcha el proyecto en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone <https://github.com/TianLeblanc/GENERADOR_ANALITICO_DE_DENSIDADES_PROBABILISTICAS_DISCRETAS_CONTINUAS.git>
cd <GENERADOR_ANALITICO_DE_DENSIDADES_PROBABILISTICAS_DISCRETAS_CONTINUAS>
```

---

### 2. Crear y activar un entorno virtual (Recomendado) 
```bash
python -m venv venv
venv\Scripts\activate
```

--- 

### 3. Instalar las dependencias 
```bash
pip install -r requirements.txt
```
---
### 4. Ejecutar la Aplicación 
```bash
streamlit run app.py
```
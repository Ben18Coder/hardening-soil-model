# Modelo Hardening Soil - Calibración de Parámetros

Este proyecto implementa un sistema de calibración para el modelo constitutivo Hardening Soil, utilizado en geotecnia para simular el comportamiento no lineal de suelos.

## Características

- Calibración automática de parámetros del modelo Hardening Soil
- Visualización de curvas esfuerzo-deformación
- Generación de reportes profesionales en PDF
- Comparación entre datos experimentales y predicciones del modelo

## Estructura del Proyecto 
    hardening_soil_model/
    ├── data/ # Datos experimentales
    ├── output/
    │ ├── figures/ # Gráficas generadas
    │ └── reports/ # Reportes PDF
    ├── src/ # Código fuente
    └── main.py # Punto de entrada
## Instalación

1. Clonar el repositorio: 
bash
git clone [url-del-repositorio] (Aún no está subido a ningún repositorio)

2. Instalar dependencias:
bash
pip install -r requirements.txt

3. Ejecutar el script de calibración:
bash
python main.py

## Uso

1. Colocar los datos experimentales en la carpeta `data/`
2. Ejecutar el script de calibración:
3. Los resultados se guardarán en:
   - Gráficas: `output/figures/`
   - Reportes: `output/reports/`

## Parámetros del Modelo

El modelo calcula los siguientes parámetros:

- E50ref: Módulo de rigidez secante de referencia
- Eur_ref: Módulo de rigidez en descarga/recarga
- φ: Ángulo de fricción
- c: Cohesión
- ψ: Ángulo de dilatancia
- m: Exponente de rigidez
- ν_ur: Coeficiente de Poisson
- K0_nc: Coeficiente de empuje en reposo
- Rf: Ratio de falla

## Dependencias Principales

- numpy: Cálculos numéricos
- scipy: Optimización y ajuste de curvas
- matplotlib: Visualización de datos
- reportlab: Generación de reportes PDF
- seaborn: Mejoras visuales en gráficos

## Licencia

MIT License

Copyright (c) 2024 [Tu Nombre]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contacto

[Tu información de contacto]

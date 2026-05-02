#  Dashboard de Finanzas Personales

Un panel interactivo y visual desarrollado con **Python** y **Streamlit** para gestionar, filtrar y analizar movimientos bancarios y categorías de gastos de forma rápida y eficiente.

El objetivo de este proyecto es transformar los extractos bancarios en bruto (almacenados en Excel) en información visual clara, permitiendo entender exactamente a dónde va el dinero mes a mes.

---

## Características Principales

* **Filtros Dinámicos:** Selector de **Mes** y **Año** que actualiza instantáneamente todos los datos del reporte.
* **KPIs Inteligentes:** Tarjetas de métricas con el total de **Ingresos**, **Gastos** y **Balance**, incluyendo el cálculo del *delta* (variación porcentual o absoluta) en comparación con el mes anterior.
* **Visualización Optimizada:** Gráficos de barras limpios construidos con **Altair**, sin líneas de cuadrícula y con etiquetas de datos inteligentes:
    * **Verde** para saldos positivos y **Rojo** para saldos negativos.
    * Posicionamiento dinámico de textos para evitar superposiciones.
* **Análisis Multidimensional:**
    * **Detalle por Categoría:** Vista de ancho completo para analizar en profundidad cada tipo de gasto o ingreso.
    * **Detalle por Tipo de Movimiento y Banco:** Distribución en dos columnas paralelas para una comparativa visual ágil.
* **Identidad Visual por Entidades:** Colores corporativos personalizados para los bancos más comunes (Caixa, ING, MyInvestor, Trade Republic, etc.).

---

## Stack Tecnológico

* **Python 3.11+**
* **Streamlit** (Interfaz de usuario y despliegue del dashboard)
* **Pandas** (Procesamiento y manipulación de datos)
* **Altair** (Visualizaciones interactivas y personalizadas)
* **OpenPyXL** (Lectura de archivos Excel)

---

## Estructura del Proyecto
DashboardFinanzas/
│
├── data/                 # Archivos de datos y extractos bancarios
│   └── BBDBancos.xlsx    # Datos principal de movimientos
│
├── venv/                 # Entorno virtual de Python
├── .gitignore            # Archivos y carpetas excluidos del control de versiones
├── LICENSE               # Licencia del proyecto
├── main.py               # Código fuente principal de la aplicación Streamlit
└── README.md             # Documentación del proyecto
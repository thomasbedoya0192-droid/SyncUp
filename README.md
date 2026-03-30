# SyncUp

# 🚀 SyncUp: Gestión Dinámica de Equipos y Cronogramas

SyncUp es una aplicación de escritorio desarrollada en Python diseñada para optimizar la asignación de tareas en trabajos grupales. Utilizando algoritmos de diseño (Backtracking y Merge Sort), la aplicación evalúa la disponibilidad cruzada de los miembros del equipo, las dependencias entre tareas y sus prioridades para generar un cronograma maestro sin solapamientos, exportable a PDF.

Este proyecto fue desarrollado como parte de la asignatura de Análisis y Diseño de Algoritmos (ADA).

## ✨ Características Principales

* **Gestión Dinámica de Usuarios:** Permite agregar una cantidad flexible de integrantes al equipo, cada uno con su propio rango horario.
* **Matriz de Disponibilidad Personalizada:** Interfaz visual para marcar horas exactas en las que cada usuario tiene clases o no está disponible.
* **Motor Algorítmico:** * Ordenamiento de tareas por prioridad usando **Merge Sort**.
    * Asignación de horarios libres resolviendo restricciones y dependencias mediante **Backtracking**.
* **Interfaz Gráfica Moderna:** Desarrollada con CustomTkinter para una experiencia de usuario fluida y estética.
* **Exportación Profesional:** Generación automática de reportes del cronograma final en formato PDF.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Interfaz Gráfica (GUI):** `customtkinter`
* **Generación de Reportes:** `fpdf2`
* **Algoritmia:** Backtracking, Merge Sort, Estructuras de Datos (Clases/Objetos).

---

## ⚙️ Requisitos Previos

Asegúrate de tener Python 3 instalado en tu sistema. Para evitar conflictos con los paquetes del sistema, se recomienda encarecidamente utilizar un entorno virtual (`venv`).

Las dependencias principales del proyecto son:
* `customtkinter`
* `fpdf2`

---

## 🚀 Guía de Instalación y Ejecución

Sigue estos pasos para clonar, configurar y ejecutar el proyecto en tu máquina local. Los comandos están orientados a terminales Unix/Linux.

### 1. Clonar el repositorio (o ubicarte en la carpeta del proyecto)

* `cd ruta/a/tu/carpeta/SyncUp`

### 2. Crear un Entorno Virtual
Es recomendable usar un entorno virtual para no interferir con los paquetes globales de tu distribución (especialmente en Arch Linux).
```bash
python -m venv env

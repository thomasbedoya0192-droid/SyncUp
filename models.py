import numpy as np

class Usuario:
    def __init__(self, nombre, hora_inicio=7, hora_fin=22):
        self.nombre = nombre
        self.hora_inicio = hora_inicio  # Hora que empieza a trabajar (ej: 7)
        self.hora_fin = hora_fin        # Hora que deja de trabajar (ej: 22)
        
        # Matriz de 24 filas (horas) x 7 columnas (días)
        # 0: Bloqueo (Sueño/Fuera de jornada)
        # 1: Ocupado (Clases/Compromisos)
        # 2: Libre (Disponible para tareas)
        self.disponibilidad = self._inicializar_matriz()

    def _inicializar_matriz(self):
        # Creamos una matriz llena de ceros (Bloqueado)
        matriz = np.zeros((24, 7), dtype=int)
        
        # Marcamos como "Libre" (2) el rango de horas de trabajo
        for h in range(self.hora_inicio, self.hora_fin):
            matriz[h, :] = 2
        return matriz

    def marcar_compromiso(self, dia, hora_inicio, hora_fin):
        """Marca una clase o compromiso fijo como Ocupado (1)"""
        for h in range(hora_inicio, hora_fin):
            if 0 <= h < 24 and 0 <= dia < 7:
                self.disponibilidad[h, dia] = 1

class Tarea:
    def __init__(self, id_tarea, nombre, duracion_horas, prioridad, dependencia=None):
        self.id = id_tarea  # <--- ASEGÚRATE DE QUE DIGA self.id
        self.nombre = nombre
        self.duracion_horas = duracion_horas
        self.prioridad = prioridad
        self.dependencia = dependencia
        self.bloques = []  # Para guardar los resultados del backtracking                    # Lista de tuplas [(dia, hora), ...]
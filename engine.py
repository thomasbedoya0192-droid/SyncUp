from models import Tarea

def merge_sort_tareas(lista_tareas):
    """
    Ordena las tareas de mayor a menor prioridad usando Merge Sort.
    """
    if len(lista_tareas) <= 1:
        return lista_tareas

    medio = len(lista_tareas) // 2
    izquierda = merge_sort_tareas(lista_tareas[:medio])
    derecha = merge_sort_tareas(lista_tareas[medio:])

    return _merge(izquierda, derecha)

def _merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i].prioridad >= der[j].prioridad:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def obtener_fin_dependencia(tarea_dependiente, todas_las_tareas):
    """
    Retorna el día y hora en que termina la tarea de la que depende.
    """
    if tarea_dependiente.dependencia is None:
        return (0, 0)

    padre = next((t for t in todas_las_tareas if t.id == tarea_dependiente.dependencia), None)
    
    if padre and padre.bloques:
        # Buscamos el último bloque asignado
        ultimo_bloque = max(padre.bloques, key=lambda x: (x['dia'], x['hora']))
        return (ultimo_bloque['dia'], ultimo_bloque['hora'])
    
    return (0, 0)

def es_momento_valido(dia_actual, hora_actual, dia_fin_padre, hora_fin_padre):
    """
    Verifica si el momento actual es posterior al fin de la dependencia.
    """
    if dia_actual > dia_fin_padre:
        return True
    if dia_actual == dia_fin_padre and hora_actual > hora_fin_padre:
        return True
    return False

def resolver_horario(tareas_pendientes, usuarios):
    """
    Algoritmo de Backtracking para asignar tareas a usuarios.
    """
    tareas_ordenadas = merge_sort_tareas(tareas_pendientes)
    
    def backtrack(indice_tarea):
        if indice_tarea == len(tareas_ordenadas):
            return True
        
        tarea_actual = tareas_ordenadas[indice_tarea]
        horas_por_asignar = tarea_actual.duracion_horas
        dia_limite, hora_limite = obtener_fin_dependencia(tarea_actual, tareas_ordenadas)
        
        bloques_temporales = []
        
        # Intentamos asignar los bloques necesarios
        for d in range(7):
            for h in range(24):
                # IMPORTANTE: Aquí revisamos todos los usuarios para ese bloque de tiempo
                for usuario in usuarios:
                    if horas_por_asignar > 0:
                        if usuario.disponibilidad[h, d] == 2 and es_momento_valido(d, h, dia_limite, hora_limite):
                            
                            # Asignación temporal
                            usuario.disponibilidad[h, d] = 1 
                            bloques_temporales.append({'usuario': usuario.nombre, 'dia': d, 'hora': h})
                            horas_por_asignar -= 1
                            
                            # Si completamos la tarea, intentamos con la siguiente
                            if horas_por_asignar == 0:
                                tarea_actual.bloques = bloques_temporales
                                if backtrack(indice_tarea + 1):
                                    return True
                                
                                # Si falla más adelante, BACKTRACK
                                for b in bloques_temporales:
                                    u_obj = next(u for u in usuarios if u.nombre == b['usuario'])
                                    u_obj.disponibilidad[b['hora'], b['dia']] = 2
                                tarea_actual.bloques = []
                                horas_por_asignar = tarea_actual.duracion_horas
                                # Nota: El bucle seguirá buscando otros huecos
        
        return False

    return backtrack(0)
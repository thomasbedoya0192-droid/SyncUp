from models import Usuario, Tarea
from engine import resolver_horario, merge_sort_tareas

def imprimir_resultado(tareas_ordenadas, usuarios):
    print("\n" + "="*50)
    print("      RESULTADO DEL CRONOGRAMA (SyncUp)")
    print("="*50)
    
    for tarea in tareas_ordenadas:
        if tarea.bloques:
            print(f"\n📌 TAREA: {tarea.nombre} ({tarea.duracion_horas}h)")
            print(f"   Prioridad: {tarea.prioridad}")
            # Ordenamos los bloques por tiempo para que sea legible
            bloques_ordenados = sorted(tarea.bloques, key=lambda x: (x['dia'], x['hora']))
            for b in bloques_ordenados:
                dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
                print(f"     - {dias[b['dia']]} a las {b['hora']}:00 -> Asignado a: {b['usuario']}")
        else:
            print(f"\n❌ TAREA: {tarea.nombre} - NO SE PUDO ASIGNAR (Sin espacio o error de dependencia)")
    print("\n" + "="*50)

def test_sistema():
    # 1. Creamos el equipo de 3 personas
    # Thomas trabaja de 8am a 2pm
    u1 = Usuario("Thomas", hora_inicio=8, hora_fin=14)
    # Socio A trabaja de 2pm a 8pm (14 a 20)
    u2 = Usuario("Socio_A", hora_inicio=14, hora_fin=20)
    # Socio B trabaja de 8am a 12pm (8 a 12)
    u3 = Usuario("Socio_B", hora_inicio=8, hora_fin=12)
    
    equipo = [u1, u2, u3]

    # 2. Simulamos que Thomas tiene una clase fija el Lunes (0) de 9am a 11am
    u1.marcar_compromiso(0, 9, 11)

    # 3. Definimos tareas con dependencias
    # Tarea 1: Base de Datos (ID: 101, Duración: 4h, Prioridad: 10)
    t1 = Tarea(101, "Diseño Base Datos", 4, prioridad=10)
    
    # Tarea 2: Backend (ID: 102, Duración: 3h, Prioridad: 5, DEPENDE DE 101)
    t2 = Tarea(102, "Programar API", 3, prioridad=5, dependencia=101)
    
    # Tarea 3: Frontend (ID: 103, Duración: 2h, Prioridad: 8)
    t3 = Tarea(103, "Maquetación UI", 2, prioridad=8)

    lista_tareas = [t1, t2, t3]

    print("🚀 Iniciando motor de asignación SyncUp...")
    
    # 4. Ejecutamos el motor
    exito = resolver_horario(lista_tareas, equipo)

    if exito:
        # Usamos merge_sort solo para mostrar el reporte en orden de importancia
        tareas_finales = merge_sort_tareas(lista_tareas)
        imprimir_resultado(tareas_finales, equipo)
    else:
        print("⚠️ El algoritmo no pudo encontrar una solución válida para todos los parámetros.")

if __name__ == "__main__":
    test_sistema()
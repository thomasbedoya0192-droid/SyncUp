import customtkinter as ctk
from models import Usuario, Tarea
from engine import resolver_horario
from fpdf import FPDF

# --- VENTANA PARA CONFIGURAR DISPONIBILIDAD (MATRIZ) ---
class VentanaMatriz(ctk.CTkToplevel):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.title(f"Disponibilidad de {usuario.nombre}")
        self.geometry("700x600")
        self.usuario = usuario
        self.buttons = {} 
        self.grid_columnconfigure(list(range(8)), weight=1)
        self.setup_ui()

    def setup_ui(self):
        dias = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]
        for d, nombre in enumerate(dias):
            lbl = ctk.CTkLabel(self, text=nombre, font=("Arial", 12, "bold"))
            lbl.grid(row=0, column=d+1, pady=5)

        for h in range(self.usuario.hora_inicio, self.usuario.hora_fin):
            lbl_hora = ctk.CTkLabel(self, text=f"{h}:00")
            lbl_hora.grid(row=h+1, column=0, padx=5)
            for d in range(7):
                estado = self.usuario.disponibilidad[h, d]
                color = "#E74C3C" if estado == 1 else "#2ECC71"
                btn = ctk.CTkButton(self, text="", width=40, height=20, 
                                    fg_color=color, hover_color="#34495E",
                                    command=lambda h=h, d=d: self.toggle_celda(h, d))
                btn.grid(row=h+1, column=d+1, padx=2, pady=2)
                self.buttons[(h, d)] = btn

    def toggle_celda(self, h, d):
        if self.usuario.disponibilidad[h, d] == 2:
            self.usuario.disponibilidad[h, d] = 1 
            self.buttons[(h, d)].configure(fg_color="#E74C3C")
        else:
            self.usuario.disponibilidad[h, d] = 2 
            self.buttons[(h, d)].configure(fg_color="#2ECC71")

# --- APLICACIÓN PRINCIPAL ---
class SyncUpApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SyncUp - Gestión de Equipos Dinámicos")
        self.geometry("1100x850")
        
        self.usuarios_objetos = []
        self.tareas_lista = []

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.tab_users = self.tabview.add("1. Equipo")
        self.tab_tasks = self.tabview.add("2. Tareas")
        self.tab_result = self.tabview.add("3. Resultado")

        self.setup_users_tab()
        self.setup_tasks_tab()
        self.setup_result_tab()

    # --- PESTAÑA 1: EQUIPO ---
    def setup_users_tab(self):
        frame_add = ctk.CTkFrame(self.tab_users)
        frame_add.pack(pady=15, padx=20, fill="x")

        self.ent_new_name = ctk.CTkEntry(frame_add, placeholder_text="Nombre integrante", width=250)
        self.ent_new_name.pack(side="left", padx=10, pady=10)

        self.ent_new_ini = ctk.CTkEntry(frame_add, width=45); self.ent_new_ini.insert(0, "7")
        self.ent_new_ini.pack(side="left", padx=2)
        ctk.CTkLabel(frame_add, text="a").pack(side="left")
        self.ent_new_fin = ctk.CTkEntry(frame_add, width=45); self.ent_new_fin.insert(0, "22")
        self.ent_new_fin.pack(side="left", padx=2)

        btn_add = ctk.CTkButton(frame_add, text="+ Añadir", command=self.agregar_integrante_ui, fg_color="#27AE60")
        btn_add.pack(side="right", padx=10)

        self.scroll_users = ctk.CTkScrollableFrame(self.tab_users, label_text="Miembros del Equipo")
        self.scroll_users.pack(pady=10, padx=20, fill="both", expand=True)

    def agregar_integrante_ui(self):
        nombre = self.ent_new_name.get().strip()
        try:
            h_ini, h_fin = int(self.ent_new_ini.get()), int(self.ent_new_fin.get())
            if nombre:
                u = Usuario(nombre, h_ini, h_fin)
                self.usuarios_objetos.append(u)
                self.renderizar_lista_usuarios()
                self.ent_new_name.delete(0, 'end')
        except ValueError: pass

    def renderizar_lista_usuarios(self):
        for widget in self.scroll_users.winfo_children(): widget.destroy()
        for user in self.usuarios_objetos:
            row = ctk.CTkFrame(self.scroll_users); row.pack(pady=5, fill="x", padx=5)
            ctk.CTkLabel(row, text=f"👤 {user.nombre}", width=200, anchor="w", font=("Arial", 13, "bold")).pack(side="left", padx=10)
            ctk.CTkButton(row, text="Eliminar", width=80, fg_color="#C0392B", command=lambda u=user: self.eliminar_integrante(u)).pack(side="right", padx=5)
            ctk.CTkButton(row, text="Matriz", width=120, command=lambda u=user: VentanaMatriz(self, u)).pack(side="right", padx=5)

    def eliminar_integrante(self, usuario):
        self.usuarios_objetos.remove(usuario)
        self.renderizar_lista_usuarios()

    # --- PESTAÑA 2: TAREAS ---
    def setup_tasks_tab(self):
        frame_in = ctk.CTkFrame(self.tab_tasks); frame_in.pack(pady=10, padx=20, fill="x")
        self.ent_t_nom = ctk.CTkEntry(frame_in, placeholder_text="Tarea", width=200)
        self.ent_t_nom.grid(row=0, column=0, padx=5, pady=10)
        self.ent_t_dur = ctk.CTkEntry(frame_in, placeholder_text="Hrs", width=60)
        self.ent_t_dur.grid(row=0, column=1, padx=5, pady=10)
        self.ent_t_prio = ctk.CTkEntry(frame_in, placeholder_text="Prio", width=60)
        self.ent_t_prio.grid(row=0, column=2, padx=5, pady=10)
        self.ent_t_dep = ctk.CTkEntry(frame_in, placeholder_text="Dep", width=60)
        self.ent_t_dep.grid(row=0, column=3, padx=5, pady=10)
        ctk.CTkButton(frame_in, text="Añadir", command=self.agregar_tarea_gui).grid(row=0, column=4, padx=10)
        
        self.tasks_display = ctk.CTkTextbox(self.tab_tasks, height=350, font=("Courier", 12))
        self.tasks_display.pack(pady=10, padx=20, fill="both", expand=True)
        self.tasks_display.configure(state="normal")
        self.tasks_display.insert("0.0", f"{'ID':<4} | {'Tarea':<20} | {'Horas':<6} | {'Prio':<5} | {'Dep'}\n" + "-"*50 + "\n")
        self.tasks_display.configure(state="disabled")

    def agregar_tarea_gui(self):
        try:
            nombre = self.ent_t_nom.get().strip()
            dur, prio = int(self.ent_t_dur.get()), int(self.ent_t_prio.get())
            dep = int(self.ent_t_dep.get()) if self.ent_t_dep.get() else None
            if nombre:
                nuevo_id = len(self.tareas_lista) + 1
                t = Tarea(nuevo_id, nombre, dur, prio, dep)
                self.tareas_lista.append(t)
                self.tasks_display.configure(state="normal")
                dep_txt = str(dep) if dep is not None else "---"
                self.tasks_display.insert("end", f"{nuevo_id:<4} | {t.nombre[:20]:<20} | {t.duracion_horas:<6} | {t.prioridad:<5} | {dep_txt}\n")
                self.tasks_display.configure(state="disabled")
                self.ent_t_nom.delete(0, 'end'); self.ent_t_dur.delete(0, 'end'); self.ent_t_prio.delete(0, 'end'); self.ent_t_dep.delete(0, 'end')
        except ValueError: pass

    # --- PESTAÑA 3: RESULTADOS ---
    def setup_result_tab(self):
        frame_btns = ctk.CTkFrame(self.tab_result, fg_color="transparent"); frame_btns.pack(pady=20)
        ctk.CTkButton(frame_btns, text="🚀 GENERAR", command=self.ejecutar_backtracking, width=200).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text="📄 PDF", command=self.exportar_pdf, fg_color="#8E44AD", width=200).pack(side="left", padx=10)
        self.res_display = ctk.CTkTextbox(self.tab_result, height=500, font=("Arial", 13))
        self.res_display.pack(pady=10, padx=20, fill="both", expand=True)

    def ejecutar_backtracking(self):
        self.res_display.delete("0.0", "end")
        if resolver_horario(self.tareas_lista, self.usuarios_objetos):
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            self.res_display.insert("0.0", "✅ CRONOGRAMA COMPACTO\n" + "="*40 + "\n\n")
            for t in self.tareas_lista:
                self.res_display.insert("end", f"📌 TAREA: {t.nombre.upper()}\n")
                bloques_u = {}
                for b in t.bloques: bloques_u.setdefault(b['usuario'], []).append(b)
                for user, blocks in bloques_u.items():
                    blocks.sort(key=lambda x: (x['dia'], x['hora']))
                    i = 0
                    while i < len(blocks):
                        ini = blocks[i]
                        fin = blocks[i]
                        while (i+1 < len(blocks) and blocks[i+1]['dia'] == ini['dia'] and blocks[i+1]['hora'] == fin['hora']+1):
                            fin = blocks[i+1]
                            i += 1
                        self.res_display.insert("end", f"   ➜ {dias[ini['dia']]} {ini['hora']}:00 - {fin['hora']+1}:00 | {user}\n")
                        i += 1
                self.res_display.insert("end", "-"*45 + "\n")
        else:
            self.res_display.insert("end", "❌ Sin solución.")

    def exportar_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="SyncUp - Reporte de Cronograma", ln=True, align='C')
        pdf.ln(10)
        dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        for t in self.tareas_lista:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt=f"TAREA: {t.nombre.upper()}", ln=True)
            pdf.set_font("Arial", size=11)
            bloques_u = {}
            for b in t.bloques: bloques_u.setdefault(b['usuario'], []).append(b)
            for user, blocks in bloques_u.items():
                blocks.sort(key=lambda x: (x['dia'], x['hora']))
                i = 0
                while i < len(blocks):
                    ini, fin = blocks[i], blocks[i]
                    while (i+1 < len(blocks) and blocks[i+1]['dia'] == ini['dia'] and blocks[i+1]['hora'] == fin['hora']+1):
                        fin = blocks[i+1]
                        i += 1
                    pdf.cell(200, 8, txt=f"   - {dias[ini['dia']]} {ini['hora']}:00 a {fin['hora']+1}:00 | Resp: {user}", ln=True)
                    i += 1
            pdf.ln(5)
        pdf.output("Reporte_SyncUp.pdf")

if __name__ == "__main__":
    app = SyncUpApp()
    app.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk
from backend1 import Sistema, Estudiante, Beneficiario, Solicitud

# CONFIGURACIÓN DE ESTILO
STYLE_CONFIG = {
    "primary": "#2c3e50",
    "secondary": "#34495e",
    "accent": "#3498db",
    "bg": "#ecf0f1",
    "text": "#2c3e50",
    "white": "#ffffff",
    "font_main": ("Segoe UI", 10),
    "font_header": ("Segoe UI", 18, "bold"),
    "btn_width": 25
}

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("RedImpulso  Gestión de Servicio Social")
        self.root.geometry("1000x700")
        self.root.configure(bg=STYLE_CONFIG["bg"])
        
        self.sistema = Sistema()
        self.usuario_actual = None
        
        self.style = ttk.Style()
        self.setup_styles()
        
        self.main_container = tk.Frame(self.root, bg=STYLE_CONFIG["bg"])
        self.main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        self.mostrar_login()

    def setup_styles(self):
        self.style.theme_use('clam')
        
        self.style.configure("Treeview", 
                             background="#ffffff", 
                             foreground="#2c3e50", 
                             rowheight=30, 
                             fieldbackground="#ffffff", 
                             font=STYLE_CONFIG["font_main"])
        
        self.style.configure("Treeview.Heading", 
                             font=("Segoe UI", 10, "bold"), 
                             background="#dcdde1", 
                             foreground=STYLE_CONFIG["primary"])
        
        self.style.map("Treeview", background=[('selected', '#3498db')])
        
        # Configuración de botones y etiquetas
        self.style.configure("TButton", font=STYLE_CONFIG["font_main"], padding=8)
        self.style.configure("Header.TLabel", font=STYLE_CONFIG["font_header"], background=STYLE_CONFIG["bg"], foreground=STYLE_CONFIG["primary"])
        self.style.configure("Sub.TLabel", font=("Segoe UI", 12, "bold"), background=STYLE_CONFIG["bg"], foreground=STYLE_CONFIG["secondary"])
        self.style.configure("Form.TLabel", font=STYLE_CONFIG["font_main"], background=STYLE_CONFIG["bg"])

    def limpiar(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # LOGIN & REGISTRO
    def mostrar_login(self):
        self.limpiar()
        
        frame = tk.Frame(self.main_container, bg=STYLE_CONFIG["bg"])
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(frame, text="INICIO DE SESIÓN", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Formulario con Grid
        ttk.Label(frame, text="Correo Electrónico:", style="Form.TLabel").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.ent_correo = ttk.Entry(frame, width=35)
        self.ent_correo.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        ttk.Label(frame, text="Contraseña:", style="Form.TLabel").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        self.ent_pass = ttk.Entry(frame, width=35, show="*")
        self.ent_pass.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        btn_frame = tk.Frame(frame, bg=STYLE_CONFIG["bg"])
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="Ingresar", width=STYLE_CONFIG["btn_width"], command=self.ejecutar_login).pack(pady=5)
        ttk.Button(btn_frame, text="Crear una cuenta", width=STYLE_CONFIG["btn_width"], command=self.mostrar_registro).pack(pady=5)

    def ejecutar_login(self):
        correo = self.ent_correo.get().strip()
        password = self.ent_pass.get()
        
        if not correo or not password:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos para continuar.")
            return
            
        user = self.sistema.login(correo, password)
        if user:
            self.usuario_actual = user
            if isinstance(user, Estudiante):
                self.dashboard_estudiante()
            else:
                self.dashboard_beneficiario()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas o usuario no encontrado.")

    def mostrar_registro(self):
        self.limpiar()
        frame = tk.Frame(self.main_container, bg=STYLE_CONFIG["bg"])
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ttk.Label(frame, text="REGISTRO DE USUARIO", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        fields = [
            ("Nombre Completo:", "reg_nombre", False),
            ("Correo Electrónico:", "reg_correo", False),
            ("Contraseña:", "reg_pass", True)
        ]
        
        for i, (label_text, attr, is_pass) in enumerate(fields, start=1):
            ttk.Label(frame, text=label_text, style="Form.TLabel").grid(row=i, column=0, sticky="e", padx=10, pady=8)
            entry = ttk.Entry(frame, width=35, show="*" if is_pass else "")
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=8)
            setattr(self, attr, entry)
        
        # Selección de tipo de usuario
        ttk.Label(frame, text="Tipo de Usuario:", style="Form.TLabel").grid(row=4, column=0, sticky="e", padx=10, pady=8)
        radio_frame = tk.Frame(frame, bg=STYLE_CONFIG["bg"])
        radio_frame.grid(row=4, column=1, sticky="w", padx=10, pady=8)
        
        self.reg_tipo = tk.StringVar(value="estudiante")
        ttk.Radiobutton(radio_frame, text="Estudiante", variable=self.reg_tipo, value="estudiante").pack(side="left", padx=5)
        ttk.Radiobutton(radio_frame, text="Beneficiario", variable=self.reg_tipo, value="beneficiario").pack(side="left", padx=5)
        
        # Campo condicional de carrera
        ttk.Label(frame, text="Carrera (Opcional):", style="Form.TLabel").grid(row=5, column=0, sticky="e", padx=10, pady=8)
        self.reg_carrera = ttk.Entry(frame, width=35)
        self.reg_carrera.grid(row=5, column=1, sticky="w", padx=10, pady=8)
        
        btn_frame = tk.Frame(frame, bg=STYLE_CONFIG["bg"])
        btn_frame.grid(row=6, column=0, columnspan=2, pady=25)
        
        ttk.Button(btn_frame, text="Finalizar Registro", width=STYLE_CONFIG["btn_width"], command=self.ejecutar_registro).pack(pady=5)
        ttk.Button(btn_frame, text="Volver al Inicio", width=STYLE_CONFIG["btn_width"], command=self.mostrar_login).pack(pady=5)

    def ejecutar_registro(self):
        nombre = self.reg_nombre.get().strip()
        correo = self.reg_correo.get().strip()
        password = self.reg_pass.get()
        tipo = self.reg_tipo.get()
        carrera = self.reg_carrera.get().strip() if tipo == "estudiante" else ""
        
        if not nombre or not correo or not password:
            messagebox.showwarning("Validación", "Todos los campos principales son obligatorios.")
            return
            
        if self.sistema.registrar_usuario(nombre, correo, password, tipo, carrera):
            messagebox.showinfo("Éxito", "Usuario registrado satisfactoriamente.")
            self.mostrar_login()
        else:
            messagebox.showerror("Error", "Este correo electrónico ya se encuentra en uso.")

    #  DASHBOARD ESTUDIANTE 
    def dashboard_estudiante(self):
        self.limpiar()
        
        header = tk.Frame(self.main_container, bg=STYLE_CONFIG["bg"])
        header.pack(fill="x", pady=(0, 20))
        
        ttk.Label(header, text=f"Bienvenido, {self.usuario_actual.nombre}", style="Header.TLabel").pack(side="left")
        
        horas = self.sistema.calcular_horas(self.usuario_actual.id)
        ttk.Label(header, text=f"Horas: {horas} hrs", style="Sub.TLabel").pack(side="right", padx=10)
        
        tab_control = ttk.Notebook(self.main_container)
        tab_solicitudes = ttk.Frame(tab_control)
        tab_bitacora = ttk.Frame(tab_control)
        
        tab_control.add(tab_solicitudes, text=" Ofertas Disponibles ")
        tab_control.add(tab_bitacora, text=" Mi Diario de Actividades ")
        tab_control.pack(expand=1, fill="both")
        
        self.render_solicitudes_disponibles(tab_solicitudes)
        self.render_bitacora(tab_bitacora)
        
        ttk.Button(self.main_container, text="Cerrar Sesión", width=STYLE_CONFIG["btn_width"], command=self.mostrar_login).pack(pady=15)

    def render_solicitudes_disponibles(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        cols = ("ID", "Título", "Beneficiario", "Estado")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")
            
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        for s in self.sistema.solicitudes:
            if s.estado == "Disponible":
                nombre_ben = self.sistema.obtener_nombre_usuario(s.beneficiario_id)
                tree.insert("", "end", values=(s.id, s.titulo, nombre_ben, s.estado))
        
        def postular():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                sol_id = item['values'][0]
                if self.sistema.postular_estudiante(sol_id, self.usuario_actual.id):
                    messagebox.showinfo("Éxito", "Postulación enviada.")
                else:
                    messagebox.showinfo("Info", "Ya estás postulado a esta solicitud.")
            else:
                messagebox.showwarning("Selección", "Por favor selecciona una fila.")

        ttk.Button(parent, text="Postularme a Selección", command=postular).pack(pady=10)

    def render_bitacora(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        cols = ("ID", "Actividad", "Horas", "Fecha", "Estatus")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
            
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        for b in self.sistema.bitacoras:
            if b.estudiante_id == self.usuario_actual.id:
                tree.insert("", "end", values=(b.id, b.actividad, b.horas, b.fecha, "Listo" if b.completada else "En proceso"))

        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)
        
        def completar():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                if self.sistema.completar_actividad(item['values'][0]):
                    messagebox.showinfo("Éxito", "Estado actualizado.")
                    self.dashboard_estudiante()
            else:
                messagebox.showwarning("Selección", "Elige una actividad.")

        ttk.Button(btn_frame, text="Nueva Entrada", width=STYLE_CONFIG["btn_width"], command=self.modal_nueva_actividad).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Marcar Finalizado", width=STYLE_CONFIG["btn_width"], command=completar).pack(side="left", padx=10)

    def modal_nueva_actividad(self):
        win = tk.Toplevel(self.root)
        win.title("Nueva Actividad")
        win.geometry("400x300")
        win.configure(padx=20, pady=20)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Descripción:", style="Form.TLabel").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        ent_act = ttk.Entry(frame, width=30)
        ent_act.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        ttk.Label(frame, text="Horas:", style="Form.TLabel").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        ent_hrs = ttk.Entry(frame, width=30)
        ent_hrs.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        def guardar():
            try:
                self.sistema.registrar_actividad(self.usuario_actual.id, ent_act.get(), float(ent_hrs.get()))
                messagebox.showinfo("Éxito", "Registrado.")
                win.destroy()
                self.dashboard_estudiante()
            except ValueError:
                messagebox.showerror("Error", "Horas debe ser numérico.")

        ttk.Button(win, text="Guardar", width=STYLE_CONFIG["btn_width"], command=guardar).pack(pady=20)

    #  DASHBOARD BENEFICIARIO 
    def dashboard_beneficiario(self):
        self.limpiar()
        
        header = tk.Frame(self.main_container, bg=STYLE_CONFIG["bg"])
        header.pack(fill="x", pady=(0, 20))
        
        ttk.Label(header, text=f"Bienvenido, {self.usuario_actual.nombre}", style="Header.TLabel").pack(side="left")
        
        tab_control = ttk.Notebook(self.main_container)
        tab_mis_sol = ttk.Frame(tab_control)
        tab_control.add(tab_mis_sol, text=" Mis Publicaciones ")
        tab_control.pack(expand=1, fill="both")
        
        self.render_mis_solicitudes(tab_mis_sol)
        
        ttk.Button(self.main_container, text="Salir", width=STYLE_CONFIG["btn_width"], command=self.mostrar_login).pack(pady=15)

    def render_mis_solicitudes(self, parent):
        frame = tk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        cols = ("ID", "Título", "Estatus", "Estudiante", "Postulados")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")
            
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        for s in self.sistema.obtener_solicitudes_beneficiario(self.usuario_actual.id):
            est_nombre = self.sistema.obtener_nombre_usuario(s.estudiante_asignado_id) if s.estudiante_asignado_id else "Ninguno"
            tree.insert("", "end", values=(s.id, s.titulo, s.estado, est_nombre, len(s.postulados_ids)))
        
        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=10)

        def gestionar():
            selected = tree.selection()
            if selected:
                item = tree.item(selected[0])
                self.modal_postulados(item['values'][0])
            else:
                messagebox.showwarning("Selección", "Selecciona una fila.")

        ttk.Button(btn_frame, text="Nueva Solicitud", width=STYLE_CONFIG["btn_width"], command=self.modal_nueva_solicitud).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Ver Candidatos", width=STYLE_CONFIG["btn_width"], command=gestionar).pack(side="left", padx=10)

    def modal_nueva_solicitud(self):
        win = tk.Toplevel(self.root)
        win.title("Publicar Solicitud")
        win.geometry("500x450")
        win.configure(padx=20, pady=20)
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Título:", style="Form.TLabel").grid(row=0, column=0, sticky="ne", padx=10, pady=10)
        ent_tit = ttk.Entry(frame, width=40)
        ent_tit.grid(row=0, column=1, sticky="nw", padx=10, pady=10)
        
        ttk.Label(frame, text="Descripción:", style="Form.TLabel").grid(row=1, column=0, sticky="ne", padx=10, pady=10)
        txt_desc = tk.Text(frame, height=8, width=30, font=STYLE_CONFIG["font_main"])
        txt_desc.grid(row=1, column=1, sticky="nw", padx=10, pady=10)
        
        def guardar():
            self.sistema.crear_solicitud(ent_tit.get(), txt_desc.get("1.0", tk.END).strip(), self.usuario_actual.id)
            messagebox.showinfo("Éxito", "Publicado.")
            win.destroy()
            self.dashboard_beneficiario()

        ttk.Button(win, text="Confirmar Publicación", width=STYLE_CONFIG["btn_width"], command=guardar).pack(pady=20)

    def modal_postulados(self, solicitud_id):
        win = tk.Toplevel(self.root)
        win.title("Postulados")
        win.geometry("600x450")
        win.configure(padx=20, pady=20)
        
        sol = next(s for s in self.sistema.solicitudes if s.id == solicitud_id)
        
        ttk.Label(win, text=f"Candidatos para: {sol.titulo}", style="Sub.TLabel").pack(pady=(0, 15))
        
        frame = tk.Frame(win)
        frame.pack(fill="both", expand=True)

        cols = ("ID", "Nombre", "Carrera", "Email")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        
        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")
            
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        for p_id in sol.postulados_ids:
            nombre = self.sistema.obtener_nombre_usuario(p_id)
            contacto = self.sistema.obtener_contacto_usuario(p_id) if sol.estudiante_asignado_id == p_id else "[Protegido]"
            carrera = "N/A"
            for u in self.sistema.usuarios:
                if u.id == p_id:
                    carrera = getattr(u, "carrera", "N/A")
            tree.insert("", "end", values=(p_id, nombre, carrera, contacto))

        def asignar():
            selected = tree.selection()
            if selected:
                p_id = tree.item(selected[0])['values'][0]
                if self.sistema.asignar_estudiante(solicitud_id, p_id):
                    messagebox.showinfo("Éxito", "Asignado.")
                    win.destroy()
                    self.dashboard_beneficiario()
            else:
                messagebox.showwarning("Selección", "Elige un estudiante.")

        if sol.estado == "Disponible":
            ttk.Button(win, text="Asignar Estudiante", width=STYLE_CONFIG["btn_width"], command=asignar).pack(pady=15)
        else:
            ttk.Label(win, text="Solicitud ya asignada.", foreground="green").pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
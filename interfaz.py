import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Importamos los motores matemáticos que creaste en el paso anterior
from motores import ConjuntosEngine, BayesEngine, IndependenciaEngine

class ProbCalcApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ProbCalc Multidisciplinar v1.0")
        self.root.geometry("700x650")
        
        # Estilo visual para las pestañas
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=[10, 5])
        
        # Contenedor principal de pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear los paneles para cada pestaña
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab1, text="1. Grupos y Conjuntos")
        self.notebook.add(self.tab2, text="2. Causas y Efectos (Bayes)")
        self.notebook.add(self.tab3, text="3. Verificador de Interferencia")
        
        # Inicializar los componentes de cada pestaña
        self.construir_tab1()
        self.construir_tab2()
        self.construir_tab3()

    # -----------------------------------------------------------------
    # INTERFAZ PESTAÑA 1: TEORÍA DE CONJUNTOS
    # -----------------------------------------------------------------
    def construir_tab1(self):
        lbl_titulo = tk.Label(self.tab1, text="Análisis de Coincidencias de Grupos", font=("Arial", 13, "bold"), fg="#2c3e50")
        lbl_titulo.pack(pady=10)
        
        frame_inputs = tk.LabelFrame(self.tab1, text=" Datos de la Muestra / Encuesta ", font=("Arial", 10, "bold"))
        frame_inputs.pack(fill="x", padx=15, pady=5)
        
        tk.Label(frame_inputs, text="Total de elementos estudiados (Universo):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_universo = tk.Entry(frame_inputs, width=10)
        self.txt_universo.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_inputs, text="Elementos en el Grupo A:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_A = tk.Entry(frame_inputs, width=10)
        self.txt_A.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(frame_inputs, text="Elementos en el Grupo B:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.txt_B = tk.Entry(frame_inputs, width=10)
        self.txt_B.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(frame_inputs, text="Elementos en la Intersección (A y B):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.txt_inter = tk.Entry(frame_inputs, width=10)
        self.txt_inter.grid(row=3, column=1, padx=5, pady=5)
        
        btn_calcular = tk.Button(self.tab1, text="📊 ANALIZAR GRUPOS", bg="#3498db", fg="white", font=("Arial", 11, "bold"), command=self.calcular_tab1)
        btn_calcular.pack(fill="x", padx=15, pady=10)
        
        self.res_tab1 = tk.Text(self.tab1, height=14, font=("Consolas", 10), bg="#f8f9fa")
        self.res_tab1.pack(fill="both", expand=True, padx=15, pady=5)

    def calcular_tab1(self):
        try:
            u = int(self.txt_universo.get())
            a = int(self.txt_A.get())
            b = int(self.txt_B.get())
            i = int(self.txt_inter.get())
            
            if i > a or i > b or a > u or b > u:
                raise ValueError("Los subgrupos o la intersección exceden los límites lógicos.")
                
            # Llamada al motor estático externo
            res = ConjuntosEngine.procesar_datos(u, a, b, i)
            
            self.res_tab1.delete("1.0", tk.END)
            self.res_tab1.insert(tk.END, "============================================================\n")
            self.res_tab1.insert(tk.END, "                REPORTE DE PROBABILIDAD DE CONJUNTOS         \n")
            self.res_tab1.insert(tk.END, "============================================================\n")
            self.res_tab1.insert(tk.END, f"-> P(A) [Probabilidad de estar en Grupo A]: {res['P(A)']*100:.2f}%\n")
            self.res_tab1.insert(tk.END, f"-> P(B) [Probabilidad de estar en Grupo B]: {res['P(B)']*100:.2f}%\n")
            self.res_tab1.insert(tk.END, f"-> P(A ∩ B) [Probabilidad de estar en AMBOS]: {res['P(A n B)']*100:.2f}%\n")
            self.res_tab1.insert(tk.END, f"-> P(A ∪ B) [Probabilidad de estar en AL MENOS UNO]: {res['P(A U B)']*100:.2f}%\n")
            self.res_tab1.insert(tk.END, f"-> P(A - B) [Probabilidad de estar SOLO en A]: {res['P(A - B)']*100:.2f}%\n")
            self.res_tab1.insert(tk.END, f"-> P(B - A) [Probabilidad de estar SOLO en B]: {res['P(B - A)']*100:.2f}%\n")
            self.res_tab1.insert(tk.END, "\n[Análisis Condicional Multidisciplinar]:\n")
            self.res_tab1.insert(tk.END, f"-> P(A|B) [Si ya está en B, probabilidad de que esté en A]: {res['P(A|B)']*100:.2f}%\n")
            self.res_tab1.insert(tk.END, "============================================================\n")
        except ValueError as e:
            messagebox.showerror("Error de Datos", f"Verifique las entradas numéricas.\nDetalle: {e}")

    # -----------------------------------------------------------------
    # INTERFAZ PESTAÑA 2: TEOREMA DE BAYES
    # -----------------------------------------------------------------
    def construir_tab2(self):
        lbl_titulo = tk.Label(self.tab2, text="Análisis de Causas y Efectos (Teorema de Bayes)", font=("Arial", 13, "bold"), fg="#2c3e50")
        lbl_titulo.pack(pady=10)

        frame_config = tk.Frame(self.tab2)
        frame_config.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_config, text="¿Cuántas causas desea evaluar?:").pack(side="left")
        self.entry_num_causas = tk.Entry(frame_config, width=5)
        self.entry_num_causas.insert(0, "3")
        self.entry_num_causas.pack(side="left", padx=5)

        btn_generar = tk.Button(frame_config, text="Generar Filas", command=self.generar_campos_bayes, bg="#34495e", fg="white")
        btn_generar.pack(side="left", padx=5)

        self.frame_datos_bayes = tk.LabelFrame(self.tab2, text=" Matriz de Probabilidades (Use decimales) ")
        self.frame_datos_bayes.pack(fill="x", padx=15, pady=5)

        btn_calcular = tk.Button(self.tab2, text="⚙️ CALCULAR INFERENCIA BAYESIANA", bg="#27ae60", fg="white", font=("Arial", 11, "bold"), command=self.calcular_tab2)
        btn_calcular.pack(fill="x", padx=15, pady=5)

        self.res_tab2 = tk.Text(self.tab2, height=12, font=("Consolas", 10), bg="#f8f9fa")
        self.res_tab2.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.entradas_bayes = []
        self.generar_campos_bayes()

    def generar_campos_bayes(self):
        for fila in self.entradas_bayes:
            for widget in fila: widget.destroy()
        self.entradas_bayes.clear()

        try:
            n = int(self.entry_num_causas.get())
            if n <= 1: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero mayor a 1.")
            return

        tk.Label(self.frame_datos_bayes, text="Nombre Causa", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(self.frame_datos_bayes, text="P(Causa) [Priori]", font=("Arial", 9, "bold")).grid(row=0, column=1, padx=5)
        tk.Label(self.frame_datos_bayes, text="P(Efecto | Causa)", font=("Arial", 9, "bold")).grid(row=0, column=2, padx=5)

        for i in range(n):
            e_nom = tk.Entry(self.frame_datos_bayes, width=20)
            e_nom.insert(0, f"Causa {i+1}")
            e_nom.grid(row=i+1, column=0, padx=5, pady=2)

            e_pri = tk.Entry(self.frame_datos_bayes, width=15, justify="center")
            e_pri.grid(row=i+1, column=1, padx=5, pady=2)

            e_con = tk.Entry(self.frame_datos_bayes, width=18, justify="center")
            e_con.grid(row=i+1, column=2, padx=5, pady=2)

            self.entradas_bayes.append((e_nom, e_pri, e_con))

    def calcular_tab2(self):
        motor = BayesEngine()
        suma_p = 0.0
        try:
            for e_nom, e_pri, e_con in self.entradas_bayes:
                nom = e_nom.get()
                pri = float(e_pri.get())
                con = float(e_con.get())
                if not (0 <= pri <= 1) or not (0 <= con <= 1): raise ValueError("Probabilidades fuera del rango válido [0, 1]")
                suma_p += pri
                motor.registrar_causa(nom, pri, con)

            if abs(suma_p - 1.0) > 0.01:
                if not messagebox.askyesno("Aviso de consistencia", f"Las probabilidades prioris suman {suma_p:.2f} (No es 1.0). ¿Desea continuar?"): return

            if motor.calcular_bayes():
                self.res_tab2.delete("1.0", tk.END)
                self.res_tab2.insert(tk.END, f"============================================================\n")
                self.res_tab2.insert(tk.END, f"(*) Probabilidad Total del Efecto Observado P(E): {motor.prob_total_efecto * 100:.2f}%\n")
                self.res_tab2.insert(tk.END, f"============================================================\n")
                c_max = max(motor.causas, key=lambda x: x['posteriori'])
                for c in motor.causas:
                    self.res_tab2.insert(tk.END, f" -> P({c['nombre']} | Efecto Ocurrido): {c['posteriori']*100:.2f}%\n")
                self.res_tab2.insert(tk.END, f"\n[Conclusión Diagnóstica]: La causa raíz con mayor peso estadístico es '{c_max['nombre']}'.\n")
            else:
                messagebox.showerror("Error", "La probabilidad total del efecto es 0.")
        except ValueError as e:
            messagebox.showerror("Error", f"Error en celdas de datos.\nDetalle: {e}")

    # -----------------------------------------------------------------
    # INTERFAZ PESTAÑA 3: EVENTOS INDEPENDIENTES
    # -----------------------------------------------------------------
    def construir_tab3(self):
        lbl_titulo = tk.Label(self.tab3, text="Verificador de Interferencia (Eventos Independientes)", font=("Arial", 13, "bold"), fg="#2c3e50")
        lbl_titulo.pack(pady=10)

        frame_ind = tk.LabelFrame(self.tab3, text=" Probabilidades Teóricas ")
        frame_ind.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_ind, text="Probabilidad del Evento A - P(A):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_ind_A = tk.Entry(frame_ind, width=12)
        self.txt_ind_A.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_ind, text="Probabilidad del Evento B - P(B):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_ind_B = tk.Entry(frame_ind, width=12)
        self.txt_ind_B.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_ind, text="Probabilidad Conjunta Observada - P(A ∩ B):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.txt_ind_inter = tk.Entry(frame_ind, width=12)
        self.txt_ind_inter.grid(row=2, column=1, padx=5, pady=5)

        btn_verificar = tk.Button(self.tab3, text="🔍 EVALUAR INDEPENDENCIA", bg="#e67e22", fg="white", font=("Arial", 11, "bold"), command=self.calcular_tab3)
        btn_verificar.pack(fill="x", padx=15, pady=10)

        self.res_tab3 = tk.Text(self.tab3, height=14, font=("Consolas", 10), bg="#f8f9fa")
        self.res_tab3.pack(fill="both", expand=True, padx=15, pady=5)

    def calcular_tab3(self):
        try:
            pa = float(self.txt_ind_A.get())
            pb = float(self.txt_ind_B.get())
            pi = float(self.txt_ind_inter.get())

            if not (0 <= pa <= 1 and 0 <= pb <= 1 and 0 <= pi <= 1):
                raise ValueError("Las probabilidades deben estar estrictamente en el rango de 0 a 1.")

            # Llamada al motor de independencia
            es_ind, prod = IndependenciaEngine.verificar(pa, pb, pi)

            self.res_tab3.delete("1.0", tk.END)
            self.res_tab3.insert(tk.END, "============================================================\n")
            self.res_tab3.insert(tk.END, "              REPORTE DE INDEPENDENCIA ESTADÍSTICA          \n")
            self.res_tab3.insert(tk.END, "============================================================\n")
            self.res_tab3.insert(tk.END, f"(*) Probabilidad Conjunta Real P(A ∩ B) = {pi}\n")
            self.res_tab3.insert(tk.END, f"(*) Producto Teórico P(A) * P(B) = {pa} * {pb} = {prod:.4f}\n\n")

            if es_ind:
                self.res_tab3.insert(tk.END, "RESULTADO: Los eventos son INDEPENDIENTES.\n\n")
                self.res_tab3.insert(tk.END, "[Análisis de Variables]:\nLa ocurrencia de un evento no proporciona información sobre la \n")
                self.res_tab3.insert(tk.END, "probabilidad de ocurrencia del otro. No interfieren entre sí.\n")
            else:
                self.res_tab3.insert(tk.END, "RESULTADO: Los eventos son DEPENDIENTES.\n\n")
                self.res_tab3.insert(tk.END, "[Análisis de Variables]:\nDado que el producto difiere de la probabilidad conjunta real,\n")
                self.res_tab3.insert(tk.END, "ambos eventos tienen correlación estadística directa o indirecta.\n")
            self.res_tab3.insert(tk.END, "============================================================\n")

        except ValueError as e:
            messagebox.showerror("Error", f"Error en datos de entrada:\n{e}")
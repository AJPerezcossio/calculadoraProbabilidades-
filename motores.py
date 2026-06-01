class ConjuntosEngine:
    """Motor matemático para la teoría de conjuntos y probabilidad clásica."""
    @staticmethod
    def procesar_datos(universo_total, elementos_A, elementos_B, interseccion_AB):
        # ---------------------------------------------------------------------
        # FÓRMULA 1: REGLA DE LAPLACE (Probabilidad Clásica)
        # P(Eventos) = Casos Favorables / Casos Totales (Universo)
        # ---------------------------------------------------------------------
        p_A = elementos_A / universo_total          # P(A)
        p_B = elementos_B / universo_total          # P(B)
        p_inter = interseccion_AB / universo_total  # P(A ∩ B) - Probabilidad de la Intersección
        
        # ---------------------------------------------------------------------
        # FÓRMULA 2: TEOREMA DE LA ADICIÓN (Probabilidad de la Unión)
        # P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
        # Se restan los elementos repetidos para evitar doble contabilidad.
        # ---------------------------------------------------------------------
        p_union = p_A + p_B - p_inter
        
        # ---------------------------------------------------------------------
        # FÓRMULA 3: PROBABILIDAD DE LA DIFERENCIA
        # P(A - B) = (Elementos exclusivos de A) / Universo
        # Muestra la probabilidad de que ocurra estrictamente A, pero NO B.
        # ---------------------------------------------------------------------
        p_solo_A = (elementos_A - interseccion_AB) / universo_total
        p_solo_B = (elementos_B - interseccion_AB) / universo_total
        
        # ---------------------------------------------------------------------
        # FÓRMULA 4: PROBABILIDAD CONDICIONAL BÁSICA
        # P(A|B) = P(A ∩ B) / P(B)
        # Evalúa la probabilidad de A dado que el evento B ya ocurrió.
        # ---------------------------------------------------------------------
        p_A_dado_B = p_inter / p_B if p_B > 0 else 0
        
        # Retornamos los resultados matemáticos calculados a la interfaz
        return {
            'P(A)': p_A, 'P(B)': p_B, 'P(A n B)': p_inter,
            'P(A U B)': p_union, 'P(A - B)': p_solo_A, 'P(B - A)': p_solo_B,
            'P(A|B)': p_A_dado_B
        }


class BayesEngine:
    """Motor matemático para el Teorema de Bayes y Probabilidad Total."""
    def __init__(self):
        self.causas = []
        self.prob_total_efecto = 0.0

    def registrar_causa(self, nombre, prob_priori, prob_condicional):
        self.causas.append({
            'nombre': nombre,
            'priori': float(prob_priori),       # P(C_i) -> Probabilidad a priori
            'condicional': float(prob_condicional), # P(E|C_i) -> Probabilidad condicional
            'posteriori': 0.0                   # P(C_i|E) -> Se calculará al final con Bayes
        })

    def calcular_bayes(self):
        # ---------------------------------------------------------------------
        # FÓRMULA 5: TEOREMA DE LA PROBABILIDAD TOTAL (Denominador de Bayes)
        # P(E) = Σ [ P(C_i) * P(E|C_i) ]
        # Sumatoria del producto de cada causa por su respectiva probabilidad condicional.
        # ---------------------------------------------------------------------
        self.prob_total_efecto = sum(c['priori'] * c['condicional'] for c in self.causas)
        
        # Control de Sistemas: Evitamos división por cero si la probabilidad total es nula
        if self.prob_total_efecto == 0:
            return False
            
        # ---------------------------------------------------------------------
        # FÓRMULA 6: TEOREMA DE BAYES (Probabilidad A Posteriori)
        # P(C_k | E) = [ P(E | C_k) * P(C_k) ] / P(E)
        # Actualiza la probabilidad de la causa 'k' sabiendo que el efecto ya ocurrió.
        # ---------------------------------------------------------------------
        for c in self.causas:
            c['posteriori'] = (c['condicional'] * c['priori']) / self.prob_total_efecto
        return True


class IndependenciaEngine:
    """Motor para verificar la interferencia / independencia de eventos."""
    @staticmethod
    def verificar(p_A, p_B, p_inter):
        # ---------------------------------------------------------------------
        # FÓRMULA 7: REGLA DEL PRODUCTO PARA EVENTOS INDEPENDIENTES
        # Condición teórica: P(A ∩ B) = P(A) * P(B)
        # ---------------------------------------------------------------------
        producto = p_A * p_B
        
        # Control de Ingeniería: Debido a la pérdida de precisión de los decimales (float)
        # en hardware, restamos ambos valores y evaluamos si la diferencia es casi cero (< 0.001)
        son_independientes = abs(p_inter - producto) < 0.001
        
        return son_independientes, producto
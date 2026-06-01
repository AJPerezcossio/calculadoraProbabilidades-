class ConjuntosEngine:
    """Motor matemático para la teoría de conjuntos y probabilidad clásica."""
    @staticmethod
    def procesar_datos(universo_total, elementos_A, elementos_B, interseccion_AB):
        p_A = elementos_A / universo_total
        p_B = elementos_B / universo_total
        p_inter = interseccion_AB / universo_total
        
        # Fórmula de la Adición
        p_union = p_A + p_B - p_inter
        
        # Diferencias de conjuntos
        p_solo_A = (elementos_A - interseccion_AB) / universo_total
        p_solo_B = (elementos_B - interseccion_AB) / universo_total
        
        # Probabilidad Condicional P(A|B)
        p_A_dado_B = p_inter / p_B if p_B > 0 else 0
        
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
            'priori': float(prob_priori),
            'condicional': float(prob_condicional),
            'posteriori': 0.0
        })

    def calcular_bayes(self):
        # Teorema de la Probabilidad Total (Denominador)
        self.prob_total_efecto = sum(c['priori'] * c['condicional'] for c in self.causas)
        
        if self.prob_total_efecto == 0:
            return False
            
        # Teorema de Bayes (Actualización de probabilidades)
        for c in self.causas:
            c['posteriori'] = (c['condicional'] * c['priori']) / self.prob_total_efecto
        return True


class IndependenciaEngine:
    """Motor para verificar la interferencia / independencia de eventos."""
    @staticmethod
    def verificar(p_A, p_B, p_inter):
        producto = p_A * p_B
        # Margen de tolerancia épsilon por precisión decimal en hardware
        son_independientes = abs(p_inter - producto) < 0.001
        return son_independientes, producto
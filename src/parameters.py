from scipy.optimize import curve_fit
from scipy.stats import linregress
import numpy as np

class HardeningSoilParameters:
    #Cálculo de parámetros de resistencia
    
    @staticmethod
    def calculate_phi_and_c(confining_pressures, peak_stresses):
        slope, intercept = np.polyfit(confining_pressures, peak_stresses, 1)
        sin_phi = slope / (2 + slope)
        phi = np.degrees(np.arcsin(sin_phi))
        c = intercept * (1 - sin_phi) / (2 * np.cos(np.radians(phi)))
        return phi, c
    
    @staticmethod
    def calculate_psi(axial_strain, volumetric_strain):
        """
        Calcula el ángulo de dilatancia (ψ) usando la relación entre deformaciones.
        """
        # Identificar fase dilatante (Δε_v < 0)
        dilatant_mask = volumetric_strain < 0
        if not np.any(dilatant_mask):
            return 0.0  # Sin dilatancia
        
        delta_ev = np.diff(volumetric_strain[dilatant_mask])
        delta_e1 = np.diff(axial_strain[dilatant_mask])
        
        a = -np.mean(delta_ev / delta_e1)
        sin_psi = a / (2 + a)
        return np.degrees(np.arcsin(sin_psi))

    @staticmethod
    def calculate_E50ref(strain, stress):
        """
        Calcula el módulo secante experimental E50ref:
        Esfuerzo al 50% de la resistencia máxima / deformación correspondiente.
        """
        peak_stress = np.max(stress)  # Resistencia máxima (q_peak)
        target_stress = 0.5 * peak_stress  # 50% de q_peak
        idx = np.argmin(np.abs(stress - target_stress))  # Índice al 50% de q_peak
        return stress[idx] / strain[idx]  # E50ref = σ50 / ε50  # E50ref (experimental)

    #Cálculo de parametros hiperbolicos
    
    @staticmethod
    def calculate_m(confining_pressures, E50_values, c, phi, p_ref=100):
        """
        Calcula el exponente 'm' y E50_ref mediante regresión lineal, considerando:
        E50 = E50_ref * [(c·cosφ + σ3·sinφ) / (c·cosφ + p_ref·sinφ)]^m
        
        Retorna:
        - m: exponente de la ley potencial
        - E50_ref: módulo secante de referencia calculado del intercepto
        """
        # Convertir a arrays numpy
        sigma_3 = np.array(confining_pressures)
        E50 = np.array(E50_values)
        
        # Calcular términos del numerador y denominador
        numerator = c * np.cos(np.radians(phi)) + sigma_3 * np.sin(np.radians(phi))
        denominator = c * np.cos(np.radians(phi)) + p_ref * np.sin(np.radians(phi))
        
        # Calcular logaritmos para regresión
        log_ratio = np.log(numerator / denominator)
        log_E50 = np.log(E50)
        
        # Regresión lineal (y = m*x + b)
        slope, intercept, _, _, _ = linregress(log_ratio, log_E50)
        
        # Calcular E50_ref del intercepto
        E50_ref = np.exp(intercept)
        
        return slope, E50_ref

    @staticmethod
    def calculate_K0_nc(phi):
        return 1 - np.sin(np.radians(phi))

    @staticmethod
    def calculate_vur():
        """
        Calcula ν. (valor por defecto)
        """
        return 0.2 

    @staticmethod
    def calculate_qf(cp, c, phi):
        """
        Calcula el esfuerzo desviador en la falla (qf) usando el criterio de falla de Mohr-Coulomb.
        
        Parámetros:
        - cp: Presión de confinamiento (σ3) [kPa]
        - c: Cohesión del suelo [kPa]
        - phi: Ángulo de fricción interna [grados]
        
        Retorna:
        - qf: Esfuerzo desviador en la falla [kPa]
        
        Raises:
        - ValueError: Si alguno de los parámetros de entrada es None
        """
        # Validar que los parámetros no sean None
        if phi is None:
            raise ValueError("El parámetro 'phi' no puede ser None")
        if c is None:
            raise ValueError("El parámetro 'c' no puede ser None")
        if cp is None:
            raise ValueError("El parámetro 'cp' no puede ser None")
        
        phi_rad = np.radians(phi)
        return (2 * np.sin(phi_rad))*( cp + c/np.tan(phi_rad)) / (1 - np.sin(phi_rad))

    @staticmethod
    def calculate_Eur_ref(E50_ref):
        """
        Calcula el módulo de descarga-recarga (Eur_ref).
        Por defecto, Eur_ref = 3 * E50_ref
        
        Parámetros:
        - E50_ref: Módulo secante de referencia
        
        Retorna:
        - Eur_ref: Módulo de descarga-recarga de referencia
        """
        return 3 * E50_ref

    @staticmethod
    def calculate_Eoed_ref(E50_ref):
        """
        Calcula el módulo edométrico de referencia (Eoed_ref).
        Por defecto, Eoed_ref = E50_ref
        
        Parámetros:
        - E50_ref: Módulo secante de referencia
        
        Retorna:
        - Eoed_ref: Módulo edométrico de referencia
        """
        return E50_ref

    @staticmethod
    def calculate_qa(strain, stress):
        """
        Calcula el parámetro qa (esfuerzo asintótico) usando el método de transformación hiperbólica.
        
        El método se basa en transformar la curva esfuerzo-deformación en una relación lineal,
        graficando ε/q vs ε. En esta transformación, la pendiente 'a' de la línea recta está
        relacionada con qa mediante qa = 1/a.
        
        Parámetros:
        -----------
        strain : array_like
            Vector de deformaciones axiales (ε)
        stress : array_like
            Vector de esfuerzos desviadores (q)
        
        Retorna:
        --------
        float
            qa: Valor del esfuerzo asintótico de la hipérbola
        
        Raises:
        -------
        ValueError
            Si la pendiente es negativa o cero en la transformación hiperbólica
            Si el qa calculado es menor que el esfuerzo máximo observado
        
        Notas:
        ------
        - Solo utiliza los datos hasta el esfuerzo pico para el ajuste
        - Descarta puntos con esfuerzos menores al 10% del esfuerzo máximo
        - qa debe ser mayor que el esfuerzo máximo observado para ser físicamente válido
        """
        # Filtrar datos para usar solo la parte inicial de la curva (hasta el pico)
        peak_idx = np.argmax(stress)
        mask = slice(0, peak_idx + 1)
        
        # Calcular ε/q (evitar división por cero)
        strain_filtered = strain[mask]
        stress_filtered = stress[mask]
        
        # Eliminar puntos donde el esfuerzo es muy cercano a cero
        valid_points = stress_filtered > np.max(stress_filtered) * 0.1
        strain_filtered = strain_filtered[valid_points]
        stress_filtered = stress_filtered[valid_points]
        
        strain_stress_ratio = strain_filtered / stress_filtered
        
        # Realizar regresión lineal
        slope, intercept, r_value, _, _ = linregress(strain_filtered, strain_stress_ratio)
        
        # qa es la inversa de la pendiente
        if slope <= 0:
            raise ValueError("Error en el cálculo de qa: pendiente negativa o cero en la transformación hiperbólica")
        
        qa = 1.0 / slope
        
        # Verificar que qa sea razonable
        max_stress = np.max(stress)
        if qa < max_stress:
            raise ValueError(f"Error en el cálculo de qa: el valor calculado ({qa:.2f}) es menor que el esfuerzo máximo ({max_stress:.2f})")
        
        return qa

    @staticmethod
    def calculate_E50(E50_ref, c, phi, sigma_3, m, p_ref=100):
        """
        Calcula E50 para un sigma_3 específico usando la ley potencial:
        E50 = E50_ref * [(c·cosφ + σ3·sinφ) / (c·cosφ + p_ref·sinφ)]^m
        
        Parámetros:
        - E50_ref: Módulo secante de referencia
        - c: Cohesión
        - phi: Ángulo de fricción en grados
        - sigma_3: Presión de confinamiento
        - m: Exponente de la ley potencial
        - p_ref: Presión de referencia (default 100 kPa)
        """
        phi_rad = np.radians(phi)
        numerator = c * np.cos(phi_rad) + sigma_3 * np.sin(phi_rad)
        denominator = c * np.cos(phi_rad) + p_ref * np.sin(phi_rad)
        
        return E50_ref * ((numerator / denominator) ** m)

    @staticmethod
    def model_hyperbolic_curve(epsilon_1, sigma_3, E50_ref, c, phi, m, Rf, p_ref=100):
        """
        Modela la curva esfuerzo-deformación usando la ecuación hiperbólica.
        
        Parámetros:
        - epsilon_1: Array de deformaciones axiales
        - sigma_3: Presión de confinamiento
        - E50_ref: Módulo secante de referencia
        - c: Cohesión
        - phi: Ángulo de fricción en grados
        - m: Exponente de la ley potencial
        - Rf: Factor de falla (promedio de todos los ensayos)
        - p_ref: Presión de referencia (default 100 kPa)
        
        Retorna:
        - Array de esfuerzos desviadores (sigma_d)
        """
        # Calcular qf para este sigma_3
        qf = HardeningSoilParameters.calculate_qf(sigma_3, c, phi)
        
        # Calcular qa usando Rf
        qa = qf / Rf
        
        # Calcular E50 para este sigma_3
        E50 = HardeningSoilParameters.calculate_E50(E50_ref, c, phi, sigma_3, m, p_ref)
        
        # Evitar división por cero cuando epsilon_1 es 0
        epsilon_1 = np.maximum(epsilon_1, 1e-10)  # Usar un valor muy pequeño en lugar de 0
        
        # Calcular sigma_d usando la ecuación hiperbólica
        sigma_d = qa / (1 + qa/ (2 * E50 * epsilon_1))
        
        return sigma_d
    
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rc
from .parameters import HardeningSoilParameters

class Visualizer:
    @staticmethod
    def plot_stress_strain(tests, save_path='output/figures/stress_strain.png'):
        # Configuración para usar mathtext
        plt.rcParams.update({
            "mathtext.fontset": "stix",
            "font.family": "STIXGeneral",
            "figure.dpi": 300,
        })
        sns.set_style("darkgrid")
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = sns.color_palette("deep")
        
        for i, (name, test) in enumerate(tests.items()):
            # Datos experimentales
            ax.scatter(test['strain'], test['stress'], 
                      color=colors[i], marker='o', s=50, alpha=0.6,
                      label=f'Experimental ($\sigma_3$={name} kPa)')
            
            # Línea del modelo
            ax.plot(test['strain_model'], test['stress_model'], 
                   color=colors[i], linestyle='-', linewidth=2,
                   label=f'Modelo ($E_{{50}}^{{ref}}$={test["E50ref"]:.0f} kPa)')

        # Agregar predicción para 600 kPa
        sigma3_pred = 600  # Presión de confinamiento para predicción
        strain_pred = np.linspace(0, max([max(test['strain']) for test in tests.values()]), 100)
        
        # Obtener los parámetros del modelo del primer ensayo (deberían ser los mismos para todos)
        first_test = next(iter(tests.values()))
        E50ref = first_test['E50ref']
        c = first_test['c']
        phi = first_test['phi']
        m = first_test['m']
        Rf = first_test['Rf']
        
        # Calcular la predicción
        stress_pred = HardeningSoilParameters.model_hyperbolic_curve(
            epsilon_1=strain_pred,
            sigma_3=sigma3_pred,
            E50_ref=E50ref,
            c=c,
            phi=phi,
            m=m,
            Rf=Rf
        )
        
        # Plotear la predicción con línea punteada
        ax.plot(strain_pred, stress_pred, 
               color='k', linestyle='--', linewidth=2,
               label=f'Predicción ($\sigma_3$=600 kPa)')

        # Etiquetas con mathtext
        ax.set_xlabel(r'Deformación Axial ($\epsilon_1$) [%]', fontsize=12, fontweight='bold')
        ax.set_ylabel(r'Esfuerzo Desviador ($q$) [kPa]', fontsize=12, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=10)
        
        # Leyenda
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', 
                 fontsize=10, frameon=True, fancybox=True, shadow=True)
        
        # Título
        ax.set_title('Curvas de Esfuerzo-Deformación\nEnsayos Triaxiales', 
                    fontsize=14, fontweight='bold', pad=20)
        
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        
        # Nota a la derecha
        plt.figtext(0.98, 0.02, 
                   'Nota: Las líneas continuas representan la predicción del modelo\n'
                   'Los puntos representan datos experimentales', 
                   fontsize=8, style='italic', ha='right')
        
        plt.tight_layout()
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()

    @staticmethod
    def plot_stress_path(tests, save_path='output/figures/stress_path.png'):
        plt.rcParams.update({
            "mathtext.fontset": "stix",
            "font.family": "STIXGeneral",
            "figure.dpi": 300,
        })
        sns.set_style("darkgrid")
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = sns.color_palette("deep")
        
        for i, (name, test) in enumerate(tests.items()):
            q = test['stress']
            p = name + q / 3
            
            ax.plot(p, q, color=colors[i], linewidth=2.5,
                   label=f'$\sigma_3$={name} kPa')
            
            ax.scatter(name, 0, color=colors[i], s=100, zorder=5,
                      marker='s', label=f'Estado inicial ($\sigma_3$={name} kPa)')

        ax.set_xlabel(r'Esfuerzo Normal Medio ($p$) [kPa]', fontsize=12, fontweight='bold')
        ax.set_ylabel(r'Esfuerzo Desviador ($q$) [kPa]', fontsize=12, fontweight='bold')
        ax.tick_params(axis='both', which='major', labelsize=10)
        
        ax.set_title('Trayectorias de Esfuerzos\nEnsayos Triaxiales', 
                    fontsize=14, fontweight='bold', pad=20)
        
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left',
                 fontsize=10, frameon=True, fancybox=True, shadow=True)
        
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        
        plt.figtext(0.98, 0.02,
                   'Nota: Los cuadrados representan los estados iniciales de confinamiento\n'
                   'Las líneas muestran la evolución del estado de esfuerzos', 
                   fontsize=8, style='italic', ha='right')
        
        plt.tight_layout()
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
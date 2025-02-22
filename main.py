from src.data_loader import DataLoader
from src.parameters import HardeningSoilParameters
from src.visualization import Visualizer
from src.report_generator import ReportGenerator
import numpy as np
from pathlib import Path

def create_output_dirs():
    """Crear directorios de salida si no existen"""
    # Obtener la ruta base del proyecto
    base_path = Path(__file__).parent
    
    # Crear directorios
    figures_dir = base_path / 'output' / 'figures'
    reports_dir = base_path / 'output' / 'reports'
    
    figures_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    return base_path

def main():
    try:
        # Crear directorios y obtener ruta base
        base_path = create_output_dirs()
        
        # Definir rutas absolutas para las imágenes y reportes
        stress_strain_path = str(base_path / 'output' / 'figures' / 'stress_strain.png')
        stress_path_fig = str(base_path / 'output' / 'figures' / 'stress_path.png')
        report_path = str(base_path / 'output' / 'reports' / 'calibration_report.pdf')
        
        # Carga de datos
        data = DataLoader.load_data('E:/Mis documentos/BENJA/UNI/geogroup/hardening_soil_calibrator/data/data_ensayos_triaxiales.xlsx')
        
        tests = {}
        parameters = {
            'E50ref': None,    
            'Eur_ref': None,
            'Eoed_ref': None,
            'c': None,
            'phi': None,
            'psi': None,
            'm': None,
            'v_ur': 0.2,
            'p_ref': 100,
            'K0_nc': None,
            'Rf': [], # Cambiado a lista vacía en lugar de None
        }
        
        # Listas temporales para cálculos
        E50ref_list = []
        confining_pressures = []
        peak_stresses = []
        
        # Primera pasada: calcular phi y c
        for cp, df in data.items():
            strain = df['strain'].values
            stress = df['stress'].values
            confining_pressures.append(cp)
            peak_stresses.append(np.max(stress))
            
        # Calcular phi y c primero
        parameters['phi'], parameters['c'] = HardeningSoilParameters.calculate_phi_and_c(
            confining_pressures, 
            peak_stresses
        )
        
        # Segunda pasada: calcular parámetros individuales
        for cp, df in data.items():
            strain = df['strain'].values
            stress = df['stress'].values
            vol_strain = df['volumetric_strain'].values

            qf = HardeningSoilParameters.calculate_qf(cp, parameters['c'], parameters['phi'])
            E50ref = HardeningSoilParameters.calculate_E50ref(strain, stress)
            E50ref_list.append(E50ref)
            
            qa = HardeningSoilParameters.calculate_qa(strain, stress)
            Rf = qf/qa if qa != 0 else None
            
            Eur_ref = HardeningSoilParameters.calculate_Eur_ref(E50ref)
            Eoed_ref = HardeningSoilParameters.calculate_Eoed_ref(E50ref)
            psi = HardeningSoilParameters.calculate_psi(strain, vol_strain)
            
            tests[cp] = {
                'strain': strain,
                'stress': stress,
                'E50ref': E50ref,
                'Eur_ref': Eur_ref,
                'Eoed_ref': Eoed_ref,
                'psi': psi,
                'qf': qf,
                'qa': qa,
                'Rf': Rf
            }
            
            if Rf is not None:
                parameters['Rf'].append(Rf)

        # Calcular todos los parámetros globales primero
        parameters['E50ref'] = np.mean(E50ref_list)
        parameters['m'], E50ref_calculated = HardeningSoilParameters.calculate_m(
            confining_pressures, 
            E50ref_list, 
            parameters['c'], 
            parameters['phi'], 
            p_ref=parameters['p_ref']
        )
        parameters['K0_nc'] = HardeningSoilParameters.calculate_K0_nc(parameters['phi'])
        parameters['psi'] = np.nanmean([test['psi'] for test in tests.values()])
        parameters['v_ur'] = np.mean(parameters['v_ur'])
        valid_Rfs = [rf for rf in parameters['Rf'] if rf is not None]
        parameters['Rf'] = np.mean(valid_Rfs)
        
        # Asignar valores por defecto
        parameters['Eoed_ref'] = parameters['E50ref']
        parameters['Eur_ref'] = 3*parameters['E50ref']

        # AHORA que tenemos todos los parámetros, hacer el modelado
        for cp in confining_pressures:
            strain_model = np.linspace(0, max(tests[cp]['strain']), 100)
            
            stress_model = HardeningSoilParameters.model_hyperbolic_curve(
                epsilon_1=strain_model,
                sigma_3=cp,
                E50_ref=E50ref_calculated,
                c=parameters['c'],
                phi=parameters['phi'],
                m=parameters['m'],
                Rf=parameters['Rf']
            )
            
            # Actualizar el diccionario tests
            tests[cp].update({
                'strain_model': strain_model,
                'stress_model': stress_model,
                'c': parameters['c'],
                'phi': parameters['phi'],
                'm': parameters['m']
            })
        
        # Visualización y reportes
        Visualizer.plot_stress_strain(tests)
        Visualizer.plot_stress_path(tests)
        ReportGenerator.generate_report(
            parameters=parameters,
            img_paths=[stress_strain_path, stress_path_fig],
            output_file=report_path
        )
        
    except ValueError as e:
        print(f"Error en los parámetros: {e}")
        return
    except Exception as e:
        print(f"Error inesperado: {e}")
        return

if __name__ == "__main__":
    main()
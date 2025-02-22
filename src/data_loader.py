import pandas as pd
import numpy as np

class DataLoader:
    @staticmethod
    def load_data(file_path):
        """
        Carga datos de un ensayo triaxial desde un archivo Excel.
        
        Args:
            file_path (str): Ruta al archivo Excel.
        
        Returns:
            dict: Diccionario con DataFrames agrupados por presión de confinamiento.
        
        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si faltan columnas o hay datos inválidos.
        """
        try:
            df = pd.read_excel(file_path)
            # Modificar las columnas requeridas para incluir deformación volumétrica
            required_cols = {'strain', 'stress', 'confining_pressure', 'volumetric_strain'}
            
            # Verificar columnas requeridas
            if not all(col in df.columns for col in required_cols):
                missing = [col for col in required_cols if col not in df.columns]
                raise ValueError(f"Columnas faltantes: {missing}")
            
            # Verificar datos faltantes
            if df[list(required_cols)].isnull().any().any():
                raise ValueError("Datos con valores faltantes.")
            
            # Agrupar por presión de confinamiento
            grouped = {name: group for name, group in df.groupby('confining_pressure')}
            return grouped
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo {file_path} no encontrado.")
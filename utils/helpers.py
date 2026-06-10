from pathlib import Path
import pandas as pd
import fastparquet

class Helper:
    LOADERS = {
        '.csv' : pd.read_csv,
        '.xlsx' : pd.read_excel,
        '.parquet': pd.read_parquet,
        '.json': pd.read_json
    }
    
    @staticmethod
    def create_dir(output_path: Path) -> Path:
        """
            Make a directory with pathlib
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path.parent
    
    @staticmethod
    def load_file(filepath: Path):
        """
            Load file
        """
        
        suffix = filepath.suffix.lower() # .csv | .xlsx | etc.
        if suffix not in Helper.LOADERS:
            raise ValueError(
                f"Unsopported file format: {suffix}"
            )
            
        print(f'[LOAD] Loading {suffix} data ...')
        return Helper.LOADERS[suffix](filepath) # pd.read_csv(filepath)
        
        
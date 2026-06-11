from pathlib import Path
import pandas as pd
import fastparquet
from pandas import DataFrame
from datetime import datetime

class Helper:
    LOADERS = {
        '.csv' : pd.read_csv,
        '.xlsx' : pd.read_excel,
        '.parquet': pd.read_parquet,
        '.json': pd.read_json
    }
    
    @staticmethod
    def create_dir(output_path: Path | str) -> Path:
        """
            Make a directory with pathlib
        """
        output_path = Path(output_path)
            
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path.parent
    
    @staticmethod
    def load_file(filepath: Path) -> DataFrame:
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
        
    @staticmethod
    def save_to_csv(dataframe: DataFrame, output_path: Path) -> None:
        """
            save file
        """
        Helper.create_dir(output_path)
        dataframe.to_csv(output_path)
        
    @staticmethod
    def log(message: str):
        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        print(f"[INFO] {timestamp} - {message}", flush=True)
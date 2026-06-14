from abc import ABC, abstractmethod
from utils.helpers import Helper
from pathlib import Path
import pandas as pd
from pandas import DataFrame

class Load(ABC):
    @abstractmethod
    def load(self):
        pass
    
    
class TaxiLoader(Load):
    def validate_data(self, dataframe: DataFrame) -> tuple[DataFrame, DataFrame, dict]:        
        """
            Validate valid, invalid dataset
        """
        print('[VALIDATE] Validating data ...')
        
        df = dataframe.copy()
        
        # masking boolean
        duration_invalid = (df['pickup_datetime'] >= df['dropoff_datetime'])
        distance_invalid = (df['trip_distance'] <= 0)
        
        # separate data
        invalid_data = df[
            duration_invalid | distance_invalid
        ].copy() # INVALID
        
        invalid_data['error_type'] = None
        invalid_data.loc[duration_invalid, 'error_type'] = 'duration invalid'
        invalid_data.loc[distance_invalid, 'error_type'] = 'distance invalid'
        
        valid_data = df[
            ~(duration_invalid | distance_invalid)
        ].copy() # VALID
        
        stats = {
            "invalid_duration" : int(duration_invalid.sum()),
            "invalid_distance" : int(distance_invalid.sum())
        }
        
        return (
            valid_data,
            invalid_data,
            stats
        )

    def load(self, dataframe: DataFrame, output_path: Path):
        print(f'[LOAD] Loading {len(dataframe):,} rows data ...')
        Helper.save_to_csv(dataframe, output_path)
        print(f'[LOAD] Saved to {output_path} ...')
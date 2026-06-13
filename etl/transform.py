import pandas as pd
import fastparquet
from abc import ABC, abstractmethod
from pathlib import Path
from utils.helpers import Helper

# Aliases
Dataframe = pd.DataFrame

# Base Class
class Transform(ABC):

    @abstractmethod
    def transform():
        pass
    
class TaxiTransformer(Transform):
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
    
    def cleaning_data(self, dataframe: Dataframe) -> Dataframe:
        """
            Removing null values
        """
        print('[CLEAN] Removing null values ...')
        
        for col in dataframe.columns:
            if dataframe[col].dtype == "object":
                dataframe[col] = dataframe[col].fillna("Unknown")
            elif pd.api.types.is_numeric_dtype(dataframe[col]):
                dataframe[col] = dataframe[col].fillna(-999)
            elif pd.api.types.is_bool_dtype(dataframe[col]):
                pass
            
        return dataframe
    
    def standardize_dtypes(self, dataframe: Dataframe) -> Dataframe:
        """
            Transforming and Standarized dataframe
        """
        print('[STANDARDIZE] Standaring and Generaling data ...')
        
        # Renaming column
        dataframe = dataframe.rename(columns={
            'VendorID': 'vendor_id', 
            'tpep_pickup_datetime': 'pickup_datetime', 
            'tpep_dropoff_datetime': 'dropoff_datetime', 
            'RatecodeID': 'ratecode_id', 
            'PULocationID': 'pu_location_id', 
            'DOLocationID': 'do_location_id', 
            'Airport_fee': 'airport_fee'
        })
        
        # Standarization dtypes
        dataframe = dataframe.astype({
            'pickup_datetime': 'datetime64[us]',
            'dropoff_datetime': 'datetime64[us]',
            'tip_amount': 'float',
            'fare_amount': 'float',
            'total_amount': 'float',
        })        
        
        return dataframe
    
    def enrichment_data(self, dataframe: Dataframe) -> Dataframe:
        """
            Enrichment dataframe
        """
        print('[ENRICH] Enrichment data columns ...')
        
        # Create some datetime columns
        dataframe['pickup_date'] = dataframe['pickup_datetime'].dt.date
        dataframe['pickup_month'] = dataframe['pickup_datetime'].dt.month
        dataframe['pickup_month_name'] = dataframe['pickup_datetime'].dt.month_name()
        dataframe['pickup_day_of_week'] = dataframe['pickup_datetime'].dt.day_of_week
        dataframe['pickup_day_name'] = dataframe['pickup_datetime'].dt.day_name()
        dataframe['is_weekend'] = dataframe['pickup_datetime'].dt.dayofweek >= 5 # Saturday 5, Monday 6
        dataframe['time_period'] = pd.cut(
            dataframe['pickup_datetime'].dt.hour,
            bins=[-1, 5, 10, 15, 19, 23],
            labels=[
                'Late Night',
                'Morning',
                'Afternoon',
                'Evening Rush',
                'Night'
            ]
        )
        
        # Mapping payment_type and store_and_fwd_flag
        dataframe['payment_type'] = dataframe['payment_type'].replace({
            0:'Unknown',
            1:'Credit Card',
            2:'Cash',
            3:'No Charge',
            4:'Dispute'
        })
        
        dataframe['store_and_fwd_flag'] = dataframe['store_and_fwd_flag'].replace({
            'Y':'Store and Forward',
            'N':'Normal'
        })
        
        dataframe.insert(
            3,
            'trip_duration_minutes',
            (dataframe['dropoff_datetime'] - dataframe['pickup_datetime'])
                .dt.total_seconds()
                .div(60)
                .round(2)
        )
        
        return dataframe
    
    def merge_csv(self, filepath_lookup_table: str, dataframe: Dataframe) -> Dataframe: 
        """
            Merging transformed_dataframe and lookup table
        """
        print('[MERGE] Merging dataframe ...')
        
        # Load data
        output_path = (self.base_dir / ".." / "db" / "taxi" / filepath_lookup_table)
        lookup_table = Helper.load_file(output_path)
        
        # standarized columns
        pu_lookup = lookup_table.rename(columns={
            'LocationID': 'pu_location_id',
            'Borough': 'pu_borough',
            'Zone': 'pu_zone',
            'service_zone': 'pu_service_zone'
        })

        do_lookup = lookup_table.rename(columns={
            'LocationID': 'do_location_id',
            'Borough': 'do_borough',
            'Zone': 'do_zone',
            'service_zone': 'do_service_zone'
        })
        
        # merging data
        dataframe = dataframe.merge(
            pu_lookup,
            on='pu_location_id',
            how='left',
        )
        dataframe = dataframe.merge(
            do_lookup,
            on='do_location_id',
            how='left',
        )
        return dataframe
    
    def export_to_csv(self, dataframe, output_name: str) -> None:
        """
            Export dataframe to_csv
        """
        print(f'[EXPORT] Exporting {len(dataframe):,} rows data ...')
        
        output_dir = Path('data/transformed')
        output_dir.mkdir(parents=True, exist_ok=True)
        dataframe.to_csv((output_dir / output_name), index=True)

        print(f'[EXPORT] Saved to {str(output_dir) + output_name} ...')
        
    def transform(self, filepath: str, filepath_lookup_table: str, output_name: str) -> Dataframe:
        """
            Transform data
        """
            
        loaded_file = Helper.load_file(filepath)
        standardized_data = self.standardize_dtypes(loaded_file)
        transformed_data = self.enrichment_data(standardized_data)
        dataframe = self.merge_csv(filepath_lookup_table, transformed_data)
        self.export_to_csv(dataframe, output_name)
        return dataframe
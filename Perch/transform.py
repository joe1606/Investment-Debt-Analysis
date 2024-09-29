import pandas as pd
import numpy as np
from extract import extract_main
from datetime import datetime
data = extract_main()


def is_number(s):
    try:
        if isinstance(s, int) or isinstance(s, float):
            return True
    except ValueError:
        return False
    
def rename_date_columns(col):
    try:
        col_as_date = pd.to_datetime(col, errors='coerce')
        if not pd.isnull(col_as_date):
            return col_as_date.strftime('%b-%y')
    except:
        pass
    return col


def clean_title(title):
    title_mapping = {
        'Mr': 'Mr',
        'Mrs': 'Mrs',
        'Miss': 'Miss',
        'Ms': 'Ms',
        'Dr': 'Dr',
        'Doct': 'Dr'
    }

    title = title.strip().title().replace('.', '') 
    return title_mapping.get(title, title)


def calculate_age(dob_str):
    dob = pd.to_datetime(dob_str, dayfirst=True)
    today = datetime.now()
    age = today.year - dob.year - \
        ((today.month, today.day) < (dob.month, dob.day))
    return age

def clean_sale_data(sale_data):
    sale_data.columns = [rename_date_columns(col) for col in sale_data.columns] # Renamed date columns
    sale_data['Title'] = sale_data['Title'].apply(clean_title) # Cleaned titles
    sale_data['Mar-24'] = sale_data['Mar-24'].apply(
        lambda x: 0.0 if not is_number(x) else x)  # Input error on March 2024 column: X most likely meaning no payment for that month
    sale_data['Age'] = sale_data['DoB'].apply(calculate_age) # Calculate ages
    sale_data = sale_data[sale_data['Unique Reference Number'] != 16835021] # Delete row for user with clear erroneous value
    sale_data = sale_data.drop_duplicates(subset=['Unique Reference Number']) # Remove duplicate values
    return sale_data


def clean_forecasted_collections(forecasted_collections):
    forecasted_collections.columns = [rename_date_columns(col) for col 
                                      in forecasted_collections.columns] # Renamed date columns
    forecasted_collections.drop(
        'Aug-24', axis=1, inplace=True)  # Dropped first empty month
    
    forecasted_collections = forecasted_collections.drop(columns=[
                                                                 'Date '])
    
    forecasted_collections = pd.melt(forecasted_collections,
                        var_name='Date', value_name='Gross Collections')
    
    return forecasted_collections
        

def transform_main():
    sale_data = extract_main()['sale_data']
    sale_data = clean_sale_data(sale_data)

    forecasted_collections = extract_main()['forecasted_collections']
    forecasted_collections = clean_forecasted_collections(forecasted_collections)

    return {'sale_data': sale_data, 'forecasted_collections': forecasted_collections}


if __name__ == '__main__':
    transform_main()
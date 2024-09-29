import pandas as pd
import numpy as np

FILENAME = 'Investment Analyst Case Study Data.xlsx'

def import_data_from_sheet(sheet):
    return pd.read_excel(FILENAME, sheet_name=sheet, header=1)

def extract_main():
    sale_data = import_data_from_sheet('SaleFile Data')
    forecasted_collections = import_data_from_sheet('Forecasted Collections')

    return {'sale_data': sale_data, 'forecasted_collections': forecasted_collections}

if __name__ == '__main__':
    print(extract_main())
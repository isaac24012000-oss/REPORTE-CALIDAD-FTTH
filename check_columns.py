import pandas as pd

excel_file = 'CONTROL DE AUDITORIAS.xlsx'
df_couching = pd.read_excel(excel_file, sheet_name='Couching')

print('COLUMNAS EXACTAS DE COUCHING:')
for col in df_couching.columns:
    print(f'  "{col}"')

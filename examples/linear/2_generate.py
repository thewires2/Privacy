from pathlib import Path
import pandas as pd
from privacyHE import initialize, encrypt, load_public_key, load_relin_keys


initialize('float')
load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')
Path('inputs').mkdir(exist_ok=True)

df =pd.read_csv("C:\\Users\\arnav\\Downloads\\salary_data.csv", index_col = False)

new_df = pd.DataFrame()

columns = list(df.columns)

for column in columns:
    # print(column)
    x=[]
    for index,entry in enumerate(list(df[column])):
        encrypt(entry).save(f'inputs{column}/y-{index}.dat')
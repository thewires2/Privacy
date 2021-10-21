import pandas as pd
from pathlib import Path
from privacyHE import encrypt, initialize, load_public_key, load_relin_keys, display_config

initialize("float")
load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')
display_config()


df = pd.read_excel("C:\\Users\\arnav\\Downloads\\accounts.xlsx")
Path('inputs').mkdir(exist_ok=True)


for index, row in df.iterrows():
    entry = row['Revenue']
    encrypted = encrypt(entry)
    encrypted.save(f'inputs/{index}.dat')
    print(f'[CLIENT] Input {entry} encrypted to inputs/{index}.dat')

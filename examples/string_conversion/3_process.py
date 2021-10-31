import numpy as np
import pandas as pd
from privacyHE import load_public_key, load_relin_keys

load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')

df =pd.read_excel("C:\\Users\\arnav\\Downloads\\accounts.xlsx", index_col = False)

def convtostring(bits):
    chars = []
    for b in range(len(bits)//8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int("".join([str(bit) for bit in byte]),2)))
    return "".join(chars)

for index,entry in enumerate(df['Account']):
    # print(convtobits(i))
    x=np.load(f'inputs/y-{index}.npy')
    print(convtostring(x))

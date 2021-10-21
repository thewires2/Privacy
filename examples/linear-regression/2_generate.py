# Client-side 
from pathlib import Path
import numpy as np
import pandas as pd
from privacyHE import initialize, encrypt, load_public_key, load_relin_keys


initialize('float')
load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')
Path('inputs').mkdir(exist_ok=True)

df = pd.read_excel("C:\\Users\\arnav\\Downloads\\accounts.xlsx")
COEFFICIENTS = np.array(list(df['Revenue'][:3]))
def generate_point():
    xs = np.random.normal(size=3, scale=10)
    noise = np.random.normal(scale=0.2)
    y = np.inner(xs, COEFFICIENTS) + noise
    return (xs, y)


N_DATAPOINTS = 50
for i in range(N_DATAPOINTS):
    print(f'Generating datapoint {i+1} of {N_DATAPOINTS}')
    xs, y = generate_point()

    encrypt(y).save(f'inputs/y-{i}.dat')
    for j, x in enumerate(xs):
        encrypt(x).save(f'inputs/x{j}-{i}.dat')

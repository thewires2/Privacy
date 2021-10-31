import numpy as np
from pathlib import Path
from privacyHE import initialize, encrypt, load_public_key, load_relin_keys


initialize('float')
load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')
Path('inputs').mkdir(exist_ok=True)


COEFFICIENTS = np.array([3.2, -1.7, 0.8])
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
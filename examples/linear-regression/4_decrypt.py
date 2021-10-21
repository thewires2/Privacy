# Client-side script to decrypt the server's results
import numpy as np
import pandas as pd

from privacyHE import (
    initialize,
    decrypt, load_encrypted_value,
    load_private_key, load_relin_keys
)


# Initialization and keys
initialize('float')
load_private_key('keys/private.key')
load_relin_keys('keys/relin.key')


XtX = np.zeros(shape=[3, 3])
XtY = np.zeros(shape=3)
for i in range(3):
    XtY[i] = decrypt(load_encrypted_value(f'outputs/XtY-{i}.dat'))
    for j in range(3):
        XtX[i, j] = decrypt(load_encrypted_value(f'outputs/XtX-{i}-{j}.dat'))

coefficients = np.linalg.inv(XtX) @ XtY
df = pd.read_excel("C:\\Users\\arnav\\Downloads\\accounts.xlsx")
GROUND_TRUTH = list(df['Revenue'][:3])
print(GROUND_TRUTH)
for i, pair in enumerate(zip(GROUND_TRUTH, coefficients)):
    a, b = pair
    print(f'Coefficient {i}: Expected {a:.4f}, Computed {b:.4f}')

import pandas as pd
from privacyHE import (
    initialize, load_private_key, load_relin_keys,
    display_config,
    decrypt, load_encrypted_value
)

initialize("float")
load_private_key('keys/private.key')
load_relin_keys('keys/relin.key')
display_config()


# Decrypt results from the server
df = pd.read_excel("C:\\Users\\arnav\\Downloads\\accounts.xlsx")
sensitive_data=list(df['Revenue'])
for i, entry in enumerate(sensitive_data):
    encrypted = load_encrypted_value(f'outputs/{i}.dat')
    result = decrypt(encrypted)
    print(f'[CLIENT] Result for {entry}: {result}')

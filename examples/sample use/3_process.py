import os
from pathlib import Path
from privacyHE import initialize, load_public_key, load_relin_keys, display_config, load_encrypted_value

initialize("float")
load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')
display_config()

Path('outputs').mkdir(exist_ok=True)

def f(x): return x**3 - 3*x + 1 #Serverside processing

arr = os.listdir('C:\\Users\\arnav\\Desktop\\Privacy\\LIB\\PrivacyFHE\\examples\\realistic\\inputs')

for i in range(len(arr)):
    value = load_encrypted_value(f'inputs/{i}.dat')
    result = f(value) 
    result.save(f'outputs/{i}.dat')
    print(f'[SERVER] Processed entry {i}: inputs/{i}.dat -> outputs/{i}.dat')


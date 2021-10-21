from privacyHE import (
    encrypt, decrypt,
    generate_keypair,
    set_public_key, set_private_key, set_relin_keys,
    display_config
)

display_config()
public_key, private_key, relin_keys = generate_keypair()
set_public_key(public_key)
set_relin_keys(relin_keys)
display_config()
set_private_key(private_key)
display_config()


# Server
def process(x):
    return x**3 - 3*x + 1


# Client
sensitive_data = [-30, -5, 17, 28]
for entry in sensitive_data:
    encrypted = encrypt(entry) 
    result = process(encrypted) 
    print(entry, decrypt(result))

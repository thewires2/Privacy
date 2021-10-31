from pathlib import Path
import pandas as pd
import numpy as np
from privacyHE import  encrypt, load_public_key, load_relin_keys

load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')
Path('inputs').mkdir(exist_ok=True)

df = pd.read_excel("C:\\Users\\arnav\\Downloads\\accounts.xlsx", index_col = False)
# df = pd.read_csv("C:\\Users\\arnav\\Downloads\\archive\\sample.csv")

columns = list(df.columns)

def convtobits(message):
    result = []
    for i in message:
        bits = bin(ord(i))[2:]
        bits='00000000'[len(bits):]+bits
        result.extend([int(b) for b in bits])
    return result

for index,entry in enumerate(df['Account']):
    # print(convtobits(i))
    x = (convtobits(entry))
    y="".join(str(i) for i in x)
    print(entry+" Encoded to ==> "+y)
    # a=encrypt(int(y))
    # print(a)
    np.save(f'inputs/y-{index}.npy', x)

# from sklearn.feature_extraction.text import CountVectorizer
# vectorizer = CountVectorizer(stop_words="english")
# vector = vectorizer.fit_transform(df['text'])
# vector = pd.DataFrame(vector.toarray())
# for index,entry in enumerate(vector):
#     x=list(vector.iloc[index])
#     y="".join(str(i) for i in x)
#     print(entry+" Encoded to ==> "+y)
#     np.save(f'inputs/y-{index}.npy', x)
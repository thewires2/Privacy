# Server
def process(x):
    return x**3 - 3*x + 1


# Client
data = [-30, -5, 17, 28]
for i in data:
    print(i, process(i)) 

from privacyHE import initialize, load_public_key, load_relin_keys, load_encrypted_value
from pathlib import Path
initialize('float')
load_public_key('keys/public.key')
load_relin_keys('keys/relin.key')


class LinearRegression:
    def __init__(self, dimension):
        self.XtX = [[0] * dimension for i in range(dimension)]
        self.XtY = [0] * dimension
        self.dimension = dimension

    def update(self, xs, y):
        for i in range(self.dimension):
            self.XtY[i] += xs[i] * y
            for j in range(self.dimension):
                self.XtX[i][j] += xs[i] * xs[j]

    def dump(self) -> dict:
        output = {}
        for i in range(self.dimension):
            output[f'XtY-{i}'] = self.XtY[i]
            for j in range(self.dimension):
                output[f'XtX-{i}-{j}'] = self.XtX[i][j]
        return output

regression = LinearRegression(3)
N_DATAPOINTS = 50
for i in range(N_DATAPOINTS):
    xs = []
    y = load_encrypted_value(f'inputs/y-{i}.dat')
    for j in range(3):
        xs.append(load_encrypted_value(f'inputs/x{j}-{i}.dat'))
    regression.update(xs, y)
    print(f'Procesed datapoint {i+1} of {N_DATAPOINTS}')

coefficients = regression.dump()
for name, value in coefficients.items():
    value.save(f'outputs/{name}.dat')


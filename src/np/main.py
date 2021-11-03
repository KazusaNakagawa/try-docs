import numpy as np


def add(x: int, y: int) -> str:
    return np.add(x, y).tolist()


if __name__ == '__main__':
    print(add(1, 2))
    print(type(add(1, 2)))

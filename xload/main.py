from math import ceil


def parallel(a: int, b: int) -> int:
    return ceil((a * b) / (a + b))


def imparallel(a: complex, b: complex) -> complex:
    return (a * b) / (a + b)


def main():
    R = [200, 240, 300, 400, 600, 1200]
    X = [200j, 240j, 300j, 400j, 600j, 1200j]


if __name__ == "__main__":
    main()

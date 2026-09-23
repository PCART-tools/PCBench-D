def getScalarLists(N):
    return (
        ("int", [random.randint(0, 9) + 1 for _ in range(N)]),
        ("float", [1.0 - random.random() for _ in range(N)]),
        ("complex", [complex(1.0 - random.random(), 1.0 - random.random()) for _ in range(N)]),
        ("bool", [True for _ in range(N)]),
        ("mixed", [1, 2.0, 3.0 + 4.5j] + [3.0 for _ in range(N - 3)]),
        ("mixed", [True, 1, 2.0, 3.0 + 4.5j] + [3.0 for _ in range(N - 4)]),
    )

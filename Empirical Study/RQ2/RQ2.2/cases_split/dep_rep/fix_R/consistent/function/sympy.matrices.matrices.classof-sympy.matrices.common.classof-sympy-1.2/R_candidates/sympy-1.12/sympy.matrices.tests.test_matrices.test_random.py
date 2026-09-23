def test_random():
    M = randMatrix(3, 3)
    M = randMatrix(3, 3, seed=3)
    assert M == randMatrix(3, 3, seed=3)

    M = randMatrix(3, 4, 0, 150)
    M = randMatrix(3, seed=4, symmetric=True)
    assert M == randMatrix(3, seed=4, symmetric=True)

    S = M.copy()
    S.simplify()
    assert S == M  # doesn't fail when elements are Numbers, not int

    rng = random.Random(4)
    assert M == randMatrix(3, symmetric=True, prng=rng)

    # Ensure symmetry
    for size in (10, 11): # Test odd and even
        for percent in (100, 70, 30):
            M = randMatrix(size, symmetric=True, percent=percent, prng=rng)
            assert M == M.T

    M = randMatrix(10, min=1, percent=70)
    zero_count = 0
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == 0:
                zero_count += 1
    assert zero_count == 30

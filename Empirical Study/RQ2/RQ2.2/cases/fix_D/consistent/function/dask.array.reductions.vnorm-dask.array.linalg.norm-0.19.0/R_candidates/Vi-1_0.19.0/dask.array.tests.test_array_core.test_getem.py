def test_getem():
    sol = {('X', 0, 0): (getter, 'X', (slice(0, 2), slice(0, 3))),
           ('X', 1, 0): (getter, 'X', (slice(2, 4), slice(0, 3))),
           ('X', 1, 1): (getter, 'X', (slice(2, 4), slice(3, 6))),
           ('X', 0, 1): (getter, 'X', (slice(0, 2), slice(3, 6)))}
    assert getem('X', (2, 3), shape=(4, 6)) == sol

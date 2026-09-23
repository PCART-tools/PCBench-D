def test_clock_cycles():
    assert list(_clock_cycles(1, 1)) == [[(0, 0)]]
    assert list(_clock_cycles(1, 3)) == [[(0, 0)], [(0, 1)], [(0, 2)]]
    assert list(_clock_cycles(3, 1)) == [[(0, 0)], [(1, 0)], [(2, 0)]]

    assert list(_clock_cycles(3, 3)) == [
        [(0, 0)],
        [(1, 0), (0, 1)],
        [(2, 0), (1, 1), (0, 2)],
        [(2, 1), (1, 2)],
        [(2, 2)],
    ]

    assert list(_clock_cycles(4, 2)) == [
        [(0, 0)],
        [(1, 0), (0, 1)],
        [(2, 0), (1, 1)],
        [(3, 0), (2, 1)],
        [(3, 1)],
    ]

def test_quote():
    literals = [[1, 2, 3], (add, 1, 2),
                [1, [2, 3]], (add, 1, (add, 2, 3))]

    for l in literals:
        assert core.get({'x': quote(l)}, 'x') == l

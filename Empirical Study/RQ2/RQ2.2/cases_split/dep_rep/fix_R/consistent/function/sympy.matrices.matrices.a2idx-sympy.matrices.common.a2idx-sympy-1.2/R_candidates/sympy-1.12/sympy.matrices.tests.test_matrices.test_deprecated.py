def test_deprecated():
    # Maintain tests for deprecated functions.  We must capture
    # the deprecation warnings.  When the deprecated functionality is
    # removed, the corresponding tests should be removed.

    m = Matrix(3, 3, [0, 1, 0, -4, 4, 0, -2, 1, 2])
    P, Jcells = m.jordan_cells()
    assert Jcells[1] == Matrix(1, 1, [2])
    assert Jcells[0] == Matrix(2, 2, [2, 1, 0, 2])

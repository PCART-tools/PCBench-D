@XFAIL
def test_diff():
    x, y = symbols('x y')
    m = CalculusOnlyMatrix(2, 1, [x, y])
    # TODO: currently not working as ``_MinimalMatrix`` cannot be sympified:
    assert m.diff(x) == Matrix(2, 1, [1, 0])

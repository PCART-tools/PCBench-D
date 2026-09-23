def test_DeferredVector_Matrix():
    raises(TypeError, lambda: Matrix(DeferredVector("V")))

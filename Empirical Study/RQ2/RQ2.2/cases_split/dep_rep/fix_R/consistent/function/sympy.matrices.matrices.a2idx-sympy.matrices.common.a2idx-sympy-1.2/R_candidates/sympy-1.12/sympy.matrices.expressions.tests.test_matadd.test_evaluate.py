def test_evaluate():
    assert MatAdd(X, X, evaluate=True) == add(X, X, evaluate=True) == MatAdd(X, X).doit()

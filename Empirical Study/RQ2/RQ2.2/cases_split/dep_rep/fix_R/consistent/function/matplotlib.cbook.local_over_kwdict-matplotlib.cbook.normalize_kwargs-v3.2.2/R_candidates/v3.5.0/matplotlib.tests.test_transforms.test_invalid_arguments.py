def test_invalid_arguments():
    t = mtransforms.Affine2D()
    # There are two different exceptions, since the wrong number of
    # dimensions is caught when constructing an array_view, and that
    # raises a ValueError, and a wrong shape with a possible number
    # of dimensions is caught by our CALL_CPP macro, which always
    # raises the less precise RuntimeError.
    with pytest.raises(ValueError):
        t.transform(1)
    with pytest.raises(ValueError):
        t.transform([[[1]]])
    with pytest.raises(RuntimeError):
        t.transform([])
    with pytest.raises(RuntimeError):
        t.transform([1])
    with pytest.raises(RuntimeError):
        t.transform([[1]])
    with pytest.raises(RuntimeError):
        t.transform([[1, 2, 3]])

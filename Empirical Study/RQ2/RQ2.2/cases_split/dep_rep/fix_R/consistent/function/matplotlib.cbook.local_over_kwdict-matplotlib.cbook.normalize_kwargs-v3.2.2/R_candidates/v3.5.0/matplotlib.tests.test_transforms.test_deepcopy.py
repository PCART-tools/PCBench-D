def test_deepcopy():
    a = mtransforms.Affine2D()
    b = mtransforms.Affine2D()
    s = a + b
    # Updating a dependee shouldn't invalidate a deepcopy of the dependent.
    s.get_matrix()  # resolve it.
    s1 = copy.deepcopy(s)
    assert not s._invalid and not s1._invalid
    a.translate(1, 2)
    assert s._invalid and not s1._invalid
    assert (s1.get_matrix() == mtransforms.Affine2D().get_matrix()).all()
    # Updating a deepcopy of a dependee shouldn't invalidate a dependent.
    s.get_matrix()  # resolve it.
    b1 = copy.deepcopy(b)
    b1.translate(3, 4)
    assert not s._invalid
    assert (s.get_matrix() == a.get_matrix()).all()

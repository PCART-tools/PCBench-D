def test_set_offset_transform():
    with pytest.warns(MatplotlibDeprecationWarning,
                      match='.transOffset. without .offsets. has no effect'):
        mcollections.Collection([],
                                transOffset=mtransforms.IdentityTransform())

    skew = mtransforms.Affine2D().skew(2, 2)
    init = mcollections.Collection([], offsets=[], transOffset=skew)

    late = mcollections.Collection([])
    late.set_offset_transform(skew)

    assert skew == init.get_offset_transform() == late.get_offset_transform()

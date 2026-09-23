def test_intersect_2():
    """ Convert 1 D chunks"""
    old = ((20, 20, 20, 20, 20), )
    new = ((58, 4, 20, 18),)
    answer = ((((0, slice(0, 20, None)),),
            ((1, slice(0, 20, None)),),
            ((2, slice(0, 18, None)),)),
           (((2, slice(18, 20, None)),), ((3, slice(0, 2, None)),)),
           (((3, slice(2, 20, None)),), ((4, slice(0, 2, None)),)),
           (((4, slice(2, 20, None)),),))
    cross = intersect_chunks(old_chunks=old, new_chunks=new)
    assert answer == cross

def test_intersect_1():
    """ Convert 1 D chunks"""
    old=((10, 10, 10, 10, 10),)
    new = ((25, 5, 20), )
    answer = ((((0, slice(0, 10, None)),),
              ((1, slice(0, 10, None)),),
              ((2, slice(0, 5, None)),)),
             (((2, slice(5, 10, None)),),),
             (((3, slice(0, 10, None)),), ((4, slice(0, 10, None)),)))
    cross = intersect_chunks(old_chunks=old, new_chunks=new)
    assert answer == cross

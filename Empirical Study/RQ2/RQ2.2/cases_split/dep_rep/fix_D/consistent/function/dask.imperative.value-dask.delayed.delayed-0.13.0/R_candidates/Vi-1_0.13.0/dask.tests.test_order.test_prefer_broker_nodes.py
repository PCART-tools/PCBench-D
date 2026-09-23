def test_prefer_broker_nodes():
    """

    b0    b1  b2
    |      \  /
    a0      a1

    a1 should be run before a0
    """
    a, b, c = 'abc'
    dsk = {(a, 0): (f,), (a, 1): (f,),
           (b, 0): (f, (a, 0)), (b, 1): (f, (a, 1)), (b, 2): (f, (a, 1))}

    o = order(dsk)

    assert o[(a, 1)] < o[(a, 0)]

    # Switch name of 0, 1 to ensure that this isn't due to string comparison
    dsk = {(a, 0): (f,), (a, 1): (f,),
           (b, 0): (f, (a, 0)), (b, 1): (f, (a, 1)), (b, 2): (f, (a, 0))}

    o = order(dsk)

    assert o[(a, 1)] > o[(a, 0)]

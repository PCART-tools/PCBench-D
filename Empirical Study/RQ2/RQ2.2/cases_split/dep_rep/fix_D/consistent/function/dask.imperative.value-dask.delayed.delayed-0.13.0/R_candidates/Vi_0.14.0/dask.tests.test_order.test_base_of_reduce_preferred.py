def test_base_of_reduce_preferred():
    """
               a3
              /|
            a2 |
           /|  |
         a1 |  |
        /|  |  |
      a0 |  |  |
      |  |  |  |
      b0 b1 b2 b3
        \ \ / /
           c

    We really want to run b0 quickly
    """
    dsk = dict((('a', i), (f, ('a', i - 1), ('b', i))) for i in [1, 2, 3])
    dsk[('a', 0)] = (f, ('b', 0))
    dsk.update(dict((('b', i), (f, 'c', 1)) for i in [0, 1, 2, 3]))
    dsk['c'] = 1

    o = order(dsk)

    assert o == {('a', 3): 0,
                 ('a', 2): 1,
                 ('a', 1): 2,
                 ('a', 0): 3,
                 ('b', 0): 4,
                 'c': 5,
                 ('b', 1): 6,
                 ('b', 2): 7,
                 ('b', 3): 8}

    # ('b', 0) is the most important out of ('b', i)
    assert min([('b', i) for i in [0, 1, 2, 3]], key=o.get) == ('b', 0)

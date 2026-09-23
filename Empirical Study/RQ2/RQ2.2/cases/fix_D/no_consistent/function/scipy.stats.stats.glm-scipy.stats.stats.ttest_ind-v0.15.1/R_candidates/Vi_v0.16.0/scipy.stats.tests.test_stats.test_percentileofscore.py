def test_percentileofscore():
    pcos = stats.percentileofscore

    assert_equal(pcos([1,2,3,4,5,6,7,8,9,10],4), 40.0)

    for (kind, result) in [('mean', 35.0),
                           ('strict', 30.0),
                           ('weak', 40.0)]:
        yield assert_equal, pcos(np.arange(10) + 1,
                                                    4, kind=kind), \
                                                    result

    # multiple - 2
    for (kind, result) in [('rank', 45.0),
                           ('strict', 30.0),
                           ('weak', 50.0),
                           ('mean', 40.0)]:
        yield assert_equal, pcos([1,2,3,4,4,5,6,7,8,9],
                                                    4, kind=kind), \
                                                    result

    # multiple - 3
    assert_equal(pcos([1,2,3,4,4,4,5,6,7,8], 4), 50.0)
    for (kind, result) in [('rank', 50.0),
                           ('mean', 45.0),
                           ('strict', 30.0),
                           ('weak', 60.0)]:

        yield assert_equal, pcos([1,2,3,4,4,4,5,6,7,8],
                                                    4, kind=kind), \
                                                    result

    # missing
    for kind in ('rank', 'mean', 'strict', 'weak'):
        yield assert_equal, pcos([1,2,3,5,6,7,8,9,10,11],
                                                    4, kind=kind), \
                                                    30

    # larger numbers
    for (kind, result) in [('mean', 35.0),
                           ('strict', 30.0),
                           ('weak', 40.0)]:
        yield assert_equal, \
              pcos([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 40,
                   kind=kind), result

    for (kind, result) in [('mean', 45.0),
                           ('strict', 30.0),
                           ('weak', 60.0)]:
        yield assert_equal, \
              pcos([10, 20, 30, 40, 40, 40, 50, 60, 70, 80],
                   40, kind=kind), result

    for kind in ('rank', 'mean', 'strict', 'weak'):
        yield assert_equal, \
              pcos([10, 20, 30, 50, 60, 70, 80, 90, 100, 110],
                   40, kind=kind), 30.0

    # boundaries
    for (kind, result) in [('rank', 10.0),
                           ('mean', 5.0),
                           ('strict', 0.0),
                           ('weak', 10.0)]:
        yield assert_equal, \
              pcos([10, 20, 30, 50, 60, 70, 80, 90, 100, 110],
                   10, kind=kind), result

    for (kind, result) in [('rank', 100.0),
                           ('mean', 95.0),
                           ('strict', 90.0),
                           ('weak', 100.0)]:
        yield assert_equal, \
              pcos([10, 20, 30, 50, 60, 70, 80, 90, 100, 110],
                   110, kind=kind), result

    # out of bounds
    for (kind, score, result) in [('rank', 200, 100.0),
                                  ('mean', 200, 100.0),
                                  ('mean', 0, 0.0)]:
        yield assert_equal, \
              pcos([10, 20, 30, 50, 60, 70, 80, 90, 100, 110],
                   score, kind=kind), result

    assert_raises(ValueError, pcos, [1, 2, 3, 3, 4], 3, kind='unrecognized')

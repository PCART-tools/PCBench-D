def TestArgsreduce():
    a = array([1,3,2,1,2,3,3])
    b,c = argsreduce(a > 1, a, 2)

    assert_array_equal(b, [3,2,2,3,3])
    assert_array_equal(c, [2,2,2,2,2])

    b,c = argsreduce(2 > 1, a, 2)
    assert_array_equal(b, a[0])
    assert_array_equal(c, [2])

    b,c = argsreduce(a > 0, a, 2)
    assert_array_equal(b, a)
    assert_array_equal(c, [2] * numpy.size(a))

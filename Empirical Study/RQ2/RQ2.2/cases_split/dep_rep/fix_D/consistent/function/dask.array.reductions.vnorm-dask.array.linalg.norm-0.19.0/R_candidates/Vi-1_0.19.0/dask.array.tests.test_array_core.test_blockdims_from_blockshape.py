def test_blockdims_from_blockshape():
    assert blockdims_from_blockshape((10, 10), (4, 3)) == ((4, 4, 2), (3, 3, 3, 1))
    pytest.raises(TypeError, lambda: blockdims_from_blockshape((10,), None))
    assert blockdims_from_blockshape((1e2, 3), [1e1, 3]) == ((10, ) * 10, (3, ))
    assert blockdims_from_blockshape((np.int8(10), ), (5, )) == ((5, 5), )

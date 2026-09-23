def test_atop_zero_shape():
    da.atop(lambda x: x, 'i',
            da.arange(10, chunks=10), 'i',
            da.from_array(np.ones((0, 2)), ((0,), 2)), 'ab',
            da.from_array(np.ones((0,)), ((0,),)), 'a',
            dtype='float64')

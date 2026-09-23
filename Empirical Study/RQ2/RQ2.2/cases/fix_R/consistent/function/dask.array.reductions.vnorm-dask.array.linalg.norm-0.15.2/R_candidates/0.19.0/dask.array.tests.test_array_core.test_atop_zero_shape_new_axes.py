def test_atop_zero_shape_new_axes():
    da.atop(lambda x: np.ones(42), 'i',
            da.from_array(np.ones((0, 2)), ((0,), 2)), 'ab',
            da.from_array(np.ones((0,)), ((0,),)), 'a',
            dtype='float64', new_axes={'i': 42})

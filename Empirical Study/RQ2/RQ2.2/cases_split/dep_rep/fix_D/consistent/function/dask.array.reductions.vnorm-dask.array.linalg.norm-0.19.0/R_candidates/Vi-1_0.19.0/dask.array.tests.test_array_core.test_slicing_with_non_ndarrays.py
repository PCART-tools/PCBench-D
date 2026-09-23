def test_slicing_with_non_ndarrays():
    class ARangeSlice(object):
        def __init__(self, start, stop):
            self.start = start
            self.stop = stop

        def __array__(self):
            return np.arange(self.start, self.stop)

    class ARangeSlicable(object):
        dtype = np.dtype('i8')

        def __init__(self, n):
            self.n = n

        @property
        def shape(self):
            return (self.n,)

        def __getitem__(self, key):
            return ARangeSlice(key[0].start, key[0].stop)

    x = da.from_array(ARangeSlicable(10), chunks=(4,))

    assert_eq((x + 1).sum(), (np.arange(10, dtype=x.dtype) + 1).sum())

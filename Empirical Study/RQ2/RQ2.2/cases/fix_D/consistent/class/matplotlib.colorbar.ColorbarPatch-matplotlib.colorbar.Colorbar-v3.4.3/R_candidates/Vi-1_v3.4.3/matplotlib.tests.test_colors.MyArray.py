    class MyArray(np.ndarray):
        def __isub__(self, other):
            raise RuntimeError

        def __add__(self, other):
            raise RuntimeError

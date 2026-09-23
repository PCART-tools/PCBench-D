    class ArraySubclass(np.ndarray):

        def __iter__(self):
            for value in super().__iter__():
                yield np.array(value)

        def __getitem__(self, item):
            return np.array(super().__getitem__(item))

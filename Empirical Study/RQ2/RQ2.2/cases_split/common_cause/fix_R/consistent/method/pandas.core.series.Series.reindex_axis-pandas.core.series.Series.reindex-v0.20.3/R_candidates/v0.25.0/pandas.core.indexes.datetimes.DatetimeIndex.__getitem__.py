    def __getitem__(self, key):
        result = self._data.__getitem__(key)
        if is_scalar(result):
            return result
        elif result.ndim > 1:
            # To support MPL which performs slicing with 2 dim
            # even though it only has 1 dim by definition
            assert isinstance(result, np.ndarray), result
            return result
        return type(self)(result, name=self.name)

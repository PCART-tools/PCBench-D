    def __getitem__(self, key):
        result = self._data[key]
        if isinstance(result, type(self._data)):
            if result.ndim == 1:
                return type(self)(result, name=self.name)
            # Unpack to ndarray for MPL compat
            # pandas\core\indexes\extension.py:220: error: "ExtensionArray" has
            # no attribute "_data"  [attr-defined]
            result = result._data  # type: ignore[attr-defined]

        # Includes cases where we get a 2D ndarray back for MPL compat
        deprecate_ndim_indexing(result)
        return result

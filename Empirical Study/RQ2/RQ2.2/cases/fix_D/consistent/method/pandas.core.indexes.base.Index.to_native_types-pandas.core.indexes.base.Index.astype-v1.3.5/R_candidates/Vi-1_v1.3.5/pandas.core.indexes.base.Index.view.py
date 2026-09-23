    def view(self, cls=None):

        # we need to see if we are subclassing an
        # index type here
        if cls is not None and not hasattr(cls, "_typ"):
            dtype = cls
            if isinstance(cls, str):
                dtype = pandas_dtype(cls)

            if isinstance(dtype, (np.dtype, ExtensionDtype)) and needs_i8_conversion(
                dtype
            ):
                if dtype.kind == "m" and dtype != "m8[ns]":
                    # e.g. m8[s]
                    return self._data.view(cls)

                arr = self._data.view("i8")
                idx_cls = self._dtype_to_subclass(dtype)
                arr_cls = idx_cls._data_cls
                arr = arr_cls(self._data.view("i8"), dtype=dtype)
                return idx_cls._simple_new(arr, name=self.name)

            result = self._data.view(cls)
        else:
            result = self._view()
        if isinstance(result, Index):
            result._id = self._id
        return result

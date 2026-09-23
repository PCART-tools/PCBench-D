    def convert(self, copy: bool | None) -> Self:
        if copy is None:
            copy = True

        def _convert(arr):
            if is_object_dtype(arr.dtype):
                # extract NumpyExtensionArray for tests that patch
                #  NumpyExtensionArray._typ
                arr = np.asarray(arr)
                result = lib.maybe_convert_objects(
                    arr,
                    convert_non_numeric=True,
                )
                if result is arr and copy:
                    return arr.copy()
                return result
            else:
                return arr.copy() if copy else arr

        return self.apply(_convert)

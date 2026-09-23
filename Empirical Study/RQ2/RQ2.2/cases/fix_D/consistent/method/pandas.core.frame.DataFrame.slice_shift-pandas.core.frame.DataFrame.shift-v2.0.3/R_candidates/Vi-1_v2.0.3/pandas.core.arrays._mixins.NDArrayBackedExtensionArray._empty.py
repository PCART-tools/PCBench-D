    @classmethod
    def _empty(
        cls: type_t[NDArrayBackedExtensionArrayT], shape: Shape, dtype: ExtensionDtype
    ) -> NDArrayBackedExtensionArrayT:
        """
        Analogous to np.empty(shape, dtype=dtype)

        Parameters
        ----------
        shape : tuple[int]
        dtype : ExtensionDtype
        """
        # The base implementation uses a naive approach to find the dtype
        #  for the backing ndarray
        arr = cls._from_sequence([], dtype=dtype)
        backing = np.empty(shape, dtype=arr._ndarray.dtype)
        return arr._from_backing_data(backing)

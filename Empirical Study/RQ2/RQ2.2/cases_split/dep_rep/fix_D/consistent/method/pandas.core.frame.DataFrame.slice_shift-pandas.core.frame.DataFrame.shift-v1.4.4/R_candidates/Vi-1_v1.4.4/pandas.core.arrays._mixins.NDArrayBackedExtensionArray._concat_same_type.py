    @classmethod
    @doc(ExtensionArray._concat_same_type)
    def _concat_same_type(
        cls: type[NDArrayBackedExtensionArrayT],
        to_concat: Sequence[NDArrayBackedExtensionArrayT],
        axis: int = 0,
    ) -> NDArrayBackedExtensionArrayT:
        dtypes = {str(x.dtype) for x in to_concat}
        if len(dtypes) != 1:
            raise ValueError("to_concat must have the same dtype (tz)", dtypes)

        new_values = [x._ndarray for x in to_concat]
        new_values = np.concatenate(new_values, axis=axis)
        # error: Argument 1 to "_from_backing_data" of "NDArrayBackedExtensionArray" has
        # incompatible type "List[ndarray]"; expected "ndarray"
        return to_concat[0]._from_backing_data(new_values)  # type: ignore[arg-type]

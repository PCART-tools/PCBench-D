    @classmethod
    @doc(ExtensionArray._concat_same_type)
    def _concat_same_type(
        cls,
        to_concat: Sequence[Self],
        axis: AxisInt = 0,
    ) -> Self:
        if not lib.dtypes_all_equal([x.dtype for x in to_concat]):
            dtypes = {str(x.dtype) for x in to_concat}
            raise ValueError("to_concat must have the same dtype", dtypes)

        return super()._concat_same_type(to_concat, axis=axis)

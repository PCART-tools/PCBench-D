    @classmethod
    def _concat_same_type(
        cls: type[BaseMaskedArrayT],
        to_concat: Sequence[BaseMaskedArrayT],
        axis: AxisInt = 0,
    ) -> BaseMaskedArrayT:
        data = np.concatenate([x._data for x in to_concat], axis=axis)
        mask = np.concatenate([x._mask for x in to_concat], axis=axis)
        return cls(data, mask)

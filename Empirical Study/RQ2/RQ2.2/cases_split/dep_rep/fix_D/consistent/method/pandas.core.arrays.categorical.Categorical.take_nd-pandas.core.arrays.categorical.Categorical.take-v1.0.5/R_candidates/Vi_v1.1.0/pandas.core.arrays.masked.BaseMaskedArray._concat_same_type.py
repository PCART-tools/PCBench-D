    @classmethod
    def _concat_same_type(cls: Type[BaseMaskedArrayT], to_concat) -> BaseMaskedArrayT:
        data = np.concatenate([x._data for x in to_concat])
        mask = np.concatenate([x._mask for x in to_concat])
        return cls(data, mask)

    @classmethod
    def _concat_same_type(cls, to_concat) -> "PandasArray":
        return cls(np.concatenate(to_concat))

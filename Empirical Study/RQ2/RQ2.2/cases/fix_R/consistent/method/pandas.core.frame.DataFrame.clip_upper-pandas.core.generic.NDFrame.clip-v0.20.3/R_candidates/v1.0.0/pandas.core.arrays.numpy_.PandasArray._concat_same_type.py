    @classmethod
    def _concat_same_type(cls, to_concat):
        return cls(np.concatenate(to_concat))

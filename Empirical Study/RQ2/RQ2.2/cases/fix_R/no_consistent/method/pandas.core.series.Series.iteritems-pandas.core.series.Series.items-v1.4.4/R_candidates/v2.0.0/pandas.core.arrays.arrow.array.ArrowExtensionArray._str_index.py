    def _str_index(self, sub, start: int = 0, end=None):
        raise NotImplementedError(
            "str.index not supported with pd.ArrowDtype(pa.string())."
        )

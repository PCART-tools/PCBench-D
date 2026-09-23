    def _str_rindex(self, sub, start: int = 0, end=None):
        raise NotImplementedError(
            "str.rindex not supported with pd.ArrowDtype(pa.string())."
        )

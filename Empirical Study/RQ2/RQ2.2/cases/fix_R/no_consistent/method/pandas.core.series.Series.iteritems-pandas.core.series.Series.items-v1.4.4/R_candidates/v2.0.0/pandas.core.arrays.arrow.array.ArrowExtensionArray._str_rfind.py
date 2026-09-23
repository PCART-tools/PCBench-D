    def _str_rfind(self, sub, start: int = 0, end=None):
        raise NotImplementedError(
            "str.rfind not supported with pd.ArrowDtype(pa.string())."
        )

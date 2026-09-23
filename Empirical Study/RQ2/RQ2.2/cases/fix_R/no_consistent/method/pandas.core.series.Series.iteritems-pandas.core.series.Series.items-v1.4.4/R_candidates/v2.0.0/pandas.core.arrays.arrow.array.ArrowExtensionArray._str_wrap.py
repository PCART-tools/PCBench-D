    def _str_wrap(self, width, **kwargs):
        raise NotImplementedError(
            "str.wrap not supported with pd.ArrowDtype(pa.string())."
        )

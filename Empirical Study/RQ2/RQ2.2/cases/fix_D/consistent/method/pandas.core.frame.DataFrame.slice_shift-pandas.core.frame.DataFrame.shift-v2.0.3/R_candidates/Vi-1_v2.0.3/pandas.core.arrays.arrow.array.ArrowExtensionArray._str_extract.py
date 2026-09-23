    def _str_extract(self, pat: str, flags: int = 0, expand: bool = True):
        raise NotImplementedError(
            "str.extract not supported with pd.ArrowDtype(pa.string())."
        )

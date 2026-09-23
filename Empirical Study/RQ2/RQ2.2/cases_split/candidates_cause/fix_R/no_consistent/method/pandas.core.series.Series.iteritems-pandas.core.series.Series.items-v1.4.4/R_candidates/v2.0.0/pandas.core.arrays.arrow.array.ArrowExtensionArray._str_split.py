    def _str_split(
        self, pat=None, n=-1, expand: bool = False, regex: bool | None = None
    ):
        raise NotImplementedError(
            "str.split not supported with pd.ArrowDtype(pa.string())."
        )

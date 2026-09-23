    def _str_encode(self, encoding, errors: str = "strict"):
        raise NotImplementedError(
            "str.encode not supported with pd.ArrowDtype(pa.string())."
        )

    def _str_rpartition(self, sep: str, expand: bool):
        raise NotImplementedError(
            "str.rpartition not supported with pd.ArrowDtype(pa.string())."
        )

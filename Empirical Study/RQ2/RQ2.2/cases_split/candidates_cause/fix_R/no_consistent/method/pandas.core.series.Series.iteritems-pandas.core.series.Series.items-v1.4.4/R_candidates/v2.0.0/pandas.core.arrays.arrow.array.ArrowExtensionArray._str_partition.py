    def _str_partition(self, sep: str, expand: bool):
        raise NotImplementedError(
            "str.partition not supported with pd.ArrowDtype(pa.string())."
        )

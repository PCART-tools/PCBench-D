    def _str_removeprefix(self, prefix: str):
        raise NotImplementedError(
            "str.removeprefix not supported with pd.ArrowDtype(pa.string())."
        )

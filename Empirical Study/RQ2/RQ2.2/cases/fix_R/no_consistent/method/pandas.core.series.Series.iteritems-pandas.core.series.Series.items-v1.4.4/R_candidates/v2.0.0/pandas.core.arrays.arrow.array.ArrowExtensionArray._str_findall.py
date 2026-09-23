    def _str_findall(self, pat, flags: int = 0):
        raise NotImplementedError(
            "str.findall not supported with pd.ArrowDtype(pa.string())."
        )

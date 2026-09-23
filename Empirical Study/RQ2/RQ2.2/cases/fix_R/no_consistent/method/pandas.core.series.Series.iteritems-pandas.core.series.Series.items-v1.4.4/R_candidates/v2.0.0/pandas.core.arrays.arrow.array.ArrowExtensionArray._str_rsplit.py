    def _str_rsplit(self, pat=None, n=-1):
        raise NotImplementedError(
            "str.rsplit not supported with pd.ArrowDtype(pa.string())."
        )

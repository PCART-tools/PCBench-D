    def _str_normalize(self, form):
        raise NotImplementedError(
            "str.normalize not supported with pd.ArrowDtype(pa.string())."
        )

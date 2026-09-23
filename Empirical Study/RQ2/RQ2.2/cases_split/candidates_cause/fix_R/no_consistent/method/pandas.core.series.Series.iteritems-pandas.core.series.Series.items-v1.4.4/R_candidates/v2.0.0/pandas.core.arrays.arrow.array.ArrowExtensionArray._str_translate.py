    def _str_translate(self, table):
        raise NotImplementedError(
            "str.translate not supported with pd.ArrowDtype(pa.string())."
        )

    def _str_casefold(self):
        raise NotImplementedError(
            "str.casefold not supported with pd.ArrowDtype(pa.string())."
        )

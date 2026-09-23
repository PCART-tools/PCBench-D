    def _str_get_dummies(self, sep: str = "|"):
        raise NotImplementedError(
            "str.get_dummies not supported with pd.ArrowDtype(pa.string())."
        )

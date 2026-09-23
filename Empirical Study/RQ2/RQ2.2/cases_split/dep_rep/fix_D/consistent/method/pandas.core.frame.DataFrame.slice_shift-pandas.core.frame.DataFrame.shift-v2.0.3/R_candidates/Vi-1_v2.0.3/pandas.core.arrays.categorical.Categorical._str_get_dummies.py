    def _str_get_dummies(self, sep: str = "|"):
        # sep may not be in categories. Just bail on this.
        from pandas.core.arrays import PandasArray

        return PandasArray(self.astype(str))._str_get_dummies(sep)

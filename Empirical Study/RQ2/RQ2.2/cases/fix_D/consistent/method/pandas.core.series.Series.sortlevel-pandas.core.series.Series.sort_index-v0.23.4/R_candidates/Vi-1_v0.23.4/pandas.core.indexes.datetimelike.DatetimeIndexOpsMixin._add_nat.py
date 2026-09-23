    def _add_nat(self):
        """Add pd.NaT to self"""
        if is_period_dtype(self):
            raise TypeError('Cannot add {cls} and {typ}'
                            .format(cls=type(self).__name__,
                                    typ=type(NaT).__name__))

        # GH#19124 pd.NaT is treated like a timedelta for both timedelta
        # and datetime dtypes
        return self._nat_new(box=True)

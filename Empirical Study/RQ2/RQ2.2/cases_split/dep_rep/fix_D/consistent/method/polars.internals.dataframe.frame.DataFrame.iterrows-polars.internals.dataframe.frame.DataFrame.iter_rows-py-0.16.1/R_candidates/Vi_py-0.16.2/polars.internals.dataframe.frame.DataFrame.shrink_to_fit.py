    def shrink_to_fit(self: DF, in_place: bool = False) -> DF:
        """
        Shrink DataFrame memory usage.

        Shrinks to fit the exact capacity needed to hold the data.

        """
        if in_place:
            self._df.shrink_to_fit()
            return self
        else:
            df = self.clone()
            df._df.shrink_to_fit()
            return df

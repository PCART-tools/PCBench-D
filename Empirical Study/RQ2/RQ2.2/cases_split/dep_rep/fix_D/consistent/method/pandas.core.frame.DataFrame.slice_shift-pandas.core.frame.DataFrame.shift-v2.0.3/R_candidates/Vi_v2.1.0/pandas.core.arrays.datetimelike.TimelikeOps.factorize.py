    def factorize(
        self,
        use_na_sentinel: bool = True,
        sort: bool = False,
    ):
        if self.freq is not None:
            # We must be unique, so can short-circuit (and retain freq)
            codes = np.arange(len(self), dtype=np.intp)
            uniques = self.copy()  # TODO: copy or view?
            if sort and self.freq.n < 0:
                codes = codes[::-1]
                uniques = uniques[::-1]
            return codes, uniques

        if sort:
            # algorithms.factorize only passes sort=True here when freq is
            #  not None, so this should not be reached.
            raise NotImplementedError(
                f"The 'sort' keyword in {type(self).__name__}.factorize is "
                "ignored unless arr.freq is not None. To factorize with sort, "
                "call pd.factorize(obj, sort=True) instead."
            )
        return super().factorize(use_na_sentinel=use_na_sentinel)

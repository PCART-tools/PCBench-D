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
        # FIXME: shouldn't get here; we are ignoring sort
        return super().factorize(use_na_sentinel=use_na_sentinel)

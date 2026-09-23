    def sort_values(self, return_indexer=False, ascending=True):
        """
        Return sorted copy of Index.
        """
        if return_indexer:
            _as = self.argsort()
            if not ascending:
                _as = _as[::-1]
            sorted_index = self.take(_as)
            return sorted_index, _as
        else:
            # NB: using asi8 instead of _ndarray_values matters in numpy 1.18
            #  because the treatment of NaT has been changed to put NaT last
            #  instead of first.
            sorted_values = np.sort(self.asi8)
            attribs = self._get_attributes_dict()
            freq = attribs["freq"]

            if freq is not None and not is_period_dtype(self):
                if freq.n > 0 and not ascending:
                    freq = freq * -1
                elif freq.n < 0 and ascending:
                    freq = freq * -1
            attribs["freq"] = freq

            if not ascending:
                sorted_values = sorted_values[::-1]

            return self._simple_new(sorted_values, **attribs)

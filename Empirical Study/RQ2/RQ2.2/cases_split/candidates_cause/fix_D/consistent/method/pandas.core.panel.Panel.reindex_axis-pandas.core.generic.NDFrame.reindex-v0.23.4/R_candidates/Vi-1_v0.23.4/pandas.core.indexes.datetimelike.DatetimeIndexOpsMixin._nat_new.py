    def _nat_new(self, box=True):
        """
        Return Index or ndarray filled with NaT which has the same
        length as the caller.

        Parameters
        ----------
        box : boolean, default True
            - If True returns a Index as the same as caller.
            - If False returns ndarray of np.int64.
        """
        result = np.zeros(len(self), dtype=np.int64)
        result.fill(iNaT)
        if not box:
            return result

        attribs = self._get_attributes_dict()
        if not is_period_dtype(self):
            attribs['freq'] = None
        return self._simple_new(result, **attribs)

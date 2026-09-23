    def set_labels(self, labels, inplace=False, verify_integrity=True):
        """
        Set new labels on MultiIndex. Defaults to returning
        new index.

        Parameters
        ----------
        labels : sequence of arrays
            new labels to apply
        inplace : bool
            if True, mutates in place
        verify_integrity : bool (default True)
            if True, checks that levels and labels are compatible

        Returns
        -------
        new index (of same type and class...etc)
        """
        if not com.is_list_like(labels) or not com.is_list_like(labels[0]):
            raise TypeError("Labels must be list of lists-like")
        if inplace:
            idx = self
        else:
            idx = self._shallow_copy()
        idx._reset_identity()
        idx._set_labels(labels, verify_integrity=verify_integrity)
        if not inplace:
            return idx

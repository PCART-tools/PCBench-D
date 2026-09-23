    @final
    def _mask_selected_obj(self, mask: np.ndarray) -> NDFrameT:
        """
        Return _selected_obj with mask applied to the correct axis.

        Parameters
        ----------
        mask : np.ndarray
            Boolean mask to apply.

        Returns
        -------
        Series or DataFrame
            Filtered _selected_obj.
        """
        ids = self.grouper.group_info[0]
        mask = mask & (ids != -1)

        if self.axis == 0:
            return self._selected_obj[mask]
        else:
            return self._selected_obj.iloc[:, mask]

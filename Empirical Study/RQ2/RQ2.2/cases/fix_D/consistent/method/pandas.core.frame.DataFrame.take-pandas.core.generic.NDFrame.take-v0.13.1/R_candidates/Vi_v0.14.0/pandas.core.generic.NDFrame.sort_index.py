    def sort_index(self, axis=0, ascending=True):
        """
        Sort object by labels (along an axis)

        Parameters
        ----------
        axis : {0, 1}
            Sort index/rows versus columns
        ascending : boolean, default True
            Sort ascending vs. descending

        Returns
        -------
        sorted_obj : type of caller
        """
        axis = self._get_axis_number(axis)
        axis_name = self._get_axis_name(axis)
        labels = self._get_axis(axis)

        sort_index = labels.argsort()
        if not ascending:
            sort_index = sort_index[::-1]

        new_axis = labels.take(sort_index)
        return self.reindex(**{axis_name: new_axis})

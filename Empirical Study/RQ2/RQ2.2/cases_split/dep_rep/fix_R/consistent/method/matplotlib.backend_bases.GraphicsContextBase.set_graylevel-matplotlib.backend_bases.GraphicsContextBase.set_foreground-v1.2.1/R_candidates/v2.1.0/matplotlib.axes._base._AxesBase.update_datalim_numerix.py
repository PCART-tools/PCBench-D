    @cbook.deprecated('2.0', alternative='update_datalim')
    def update_datalim_numerix(self, x, y):
        """
        Update the data lim bbox with seq of xy tups
        """
        # if no data is set currently, the bbox will ignore it's
        # limits and set the bound to be the bounds of the xydata.
        # Otherwise, it will compute the bounds of it's current data
        # and the data in xydata
        if iterable(x) and not len(x):
            return
        self.dataLim.update_from_data(x, y, self.ignore_existing_data_limits)
        self.ignore_existing_data_limits = False

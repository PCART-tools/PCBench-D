    def update_datalim(self, xys, updatex=True, updatey=True):
        """
        Update the data lim bbox with seq of xy tups or equiv. 2-D array
        """
        # if no data is set currently, the bbox will ignore its
        # limits and set the bound to be the bounds of the xydata.
        # Otherwise, it will compute the bounds of it's current data
        # and the data in xydata
        xys = np.asarray(xys)
        if not len(xys):
            return
        self.dataLim.update_from_data_xy(xys, self.ignore_existing_data_limits,
                                         updatex=updatex, updatey=updatey)
        self.ignore_existing_data_limits = False

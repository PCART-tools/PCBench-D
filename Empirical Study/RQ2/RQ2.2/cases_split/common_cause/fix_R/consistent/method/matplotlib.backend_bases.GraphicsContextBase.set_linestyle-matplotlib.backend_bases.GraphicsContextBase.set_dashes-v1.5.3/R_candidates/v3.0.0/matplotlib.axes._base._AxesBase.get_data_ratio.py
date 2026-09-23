    def get_data_ratio(self):
        """
        Returns the aspect ratio of the raw data.

        This method is intended to be overridden by new projection
        types.
        """
        xmin, xmax = self.get_xbound()
        ymin, ymax = self.get_ybound()

        xsize = max(abs(xmax - xmin), 1e-30)
        ysize = max(abs(ymax - ymin), 1e-30)

        return ysize / xsize

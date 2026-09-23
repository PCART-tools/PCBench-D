    @cbook.deprecated("3.2")
    def get_data_ratio_log(self):
        """
        Return the aspect ratio of the raw data in log scale.

        Notes
        -----
        Will be used when both axis are in log scale.
        """
        xmin, xmax = self.get_xbound()
        ymin, ymax = self.get_ybound()

        xsize = max(abs(math.log10(xmax) - math.log10(xmin)), 1e-30)
        ysize = max(abs(math.log10(ymax) - math.log10(ymin)), 1e-30)

        return ysize / xsize

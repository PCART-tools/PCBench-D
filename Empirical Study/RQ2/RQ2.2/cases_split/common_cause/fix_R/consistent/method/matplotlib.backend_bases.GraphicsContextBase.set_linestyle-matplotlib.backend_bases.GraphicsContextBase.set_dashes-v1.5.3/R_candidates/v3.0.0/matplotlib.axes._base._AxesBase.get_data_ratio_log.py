    def get_data_ratio_log(self):
        """
        Returns the aspect ratio of the raw data in log scale.
        Will be used when both axis scales are in log.
        """
        xmin, xmax = self.get_xbound()
        ymin, ymax = self.get_ybound()

        xsize = max(abs(math.log10(xmax) - math.log10(xmin)), 1e-30)
        ysize = max(abs(math.log10(ymax) - math.log10(ymin)), 1e-30)

        return ysize / xsize

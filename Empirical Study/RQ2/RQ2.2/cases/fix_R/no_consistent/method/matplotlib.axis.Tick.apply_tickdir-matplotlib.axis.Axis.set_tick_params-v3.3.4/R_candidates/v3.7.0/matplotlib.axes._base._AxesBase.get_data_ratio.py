    def get_data_ratio(self):
        """
        Return the aspect ratio of the scaled data.

        Notes
        -----
        This method is intended to be overridden by new projection types.
        """
        txmin, txmax = self.xaxis.get_transform().transform(self.get_xbound())
        tymin, tymax = self.yaxis.get_transform().transform(self.get_ybound())
        xsize = max(abs(txmax - txmin), 1e-30)
        ysize = max(abs(tymax - tymin), 1e-30)
        return ysize / xsize

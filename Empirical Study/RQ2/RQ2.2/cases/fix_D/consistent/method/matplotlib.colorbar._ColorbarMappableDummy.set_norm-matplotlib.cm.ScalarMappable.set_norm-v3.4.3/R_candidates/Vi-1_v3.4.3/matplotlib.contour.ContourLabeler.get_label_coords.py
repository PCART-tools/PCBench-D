    @_api.deprecated("3.4")
    def get_label_coords(self, distances, XX, YY, ysize, lw):
        """
        Return x, y, and the index of a label location.

        Labels are plotted at a location with the smallest
        deviation of the contour from a straight line
        unless there is another label nearby, in which case
        the next best place on the contour is picked up.
        If all such candidates are rejected, the beginning
        of the contour is chosen.
        """
        hysize = int(ysize / 2)
        adist = np.argsort(distances)

        for ind in adist:
            x, y = XX[ind][hysize], YY[ind][hysize]
            if self.too_close(x, y, lw):
                continue
            return x, y, ind

        ind = adist[0]
        x, y = XX[ind][hysize], YY[ind][hysize]
        return x, y, ind

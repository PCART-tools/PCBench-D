    @staticmethod
    def span_where(x, ymin, ymax, where, **kwargs):
        """
        Create a BrokenBarHCollection to plot horizontal bars from
        over the regions in *x* where *where* is True.  The bars range
        on the y-axis from *ymin* to *ymax*

        A :class:`BrokenBarHCollection` is returned.  *kwargs* are
        passed on to the collection.
        """
        xranges = []
        for ind0, ind1 in cbook.contiguous_regions(where):
            xslice = x[ind0:ind1]
            if not len(xslice):
                continue
            xranges.append((xslice[0], xslice[-1] - xslice[0]))

        collection = BrokenBarHCollection(
            xranges, [ymin, ymax - ymin], **kwargs)
        return collection

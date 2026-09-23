    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):
        markerline, stemlines, baseline = orig_handle
        # Check to see if the stemcontainer is storing lines as a list or a
        # LineCollection. Eventually using a list will be removed, and this
        # logic can also be removed.
        using_linecoll = isinstance(stemlines, mcoll.LineCollection)

        xdata, xdata_marker = self.get_xdata(legend, xdescent, ydescent,
                                             width, height, fontsize)

        ydata = self.get_ydata(legend, xdescent, ydescent,
                               width, height, fontsize)

        if self._bottom is None:
            bottom = 0.
        else:
            bottom = self._bottom

        leg_markerline = Line2D(xdata_marker, ydata[:len(xdata_marker)])
        self.update_prop(leg_markerline, markerline, legend)

        leg_stemlines = [Line2D([x, x], [bottom, y])
                         for x, y in zip(xdata_marker, ydata)]

        if using_linecoll:
            # change the function used by update_prop() from the default
            # to one that handles LineCollection
            with cbook._setattr_cm(
                    self, _update_prop_func=self._copy_collection_props):
                for line in leg_stemlines:
                    self.update_prop(line, stemlines, legend)

        else:
            for lm, m in zip(leg_stemlines, stemlines):
                self.update_prop(lm, m, legend)

        leg_baseline = Line2D([np.min(xdata), np.max(xdata)],
                              [bottom, bottom])
        self.update_prop(leg_baseline, baseline, legend)

        artists = [*leg_stemlines, leg_baseline, leg_markerline]
        for artist in artists:
            artist.set_transform(trans)
        return artists

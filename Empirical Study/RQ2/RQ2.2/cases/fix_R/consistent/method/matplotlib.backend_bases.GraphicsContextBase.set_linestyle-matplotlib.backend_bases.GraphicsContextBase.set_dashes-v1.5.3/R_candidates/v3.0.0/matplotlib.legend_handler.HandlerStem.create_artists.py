    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):

        markerline, stemlines, baseline = orig_handle

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

        leg_stemlines = []
        for thisx, thisy in zip(xdata_marker, ydata):
            l = Line2D([thisx, thisx], [bottom, thisy])
            leg_stemlines.append(l)

        for lm, m in zip(leg_stemlines, stemlines):
            self.update_prop(lm, m, legend)

        leg_baseline = Line2D([np.min(xdata), np.max(xdata)],
                              [bottom, bottom])

        self.update_prop(leg_baseline, baseline, legend)

        artists = [leg_markerline]
        artists.extend(leg_stemlines)
        artists.append(leg_baseline)

        for artist in artists:
            artist.set_transform(trans)

        return artists

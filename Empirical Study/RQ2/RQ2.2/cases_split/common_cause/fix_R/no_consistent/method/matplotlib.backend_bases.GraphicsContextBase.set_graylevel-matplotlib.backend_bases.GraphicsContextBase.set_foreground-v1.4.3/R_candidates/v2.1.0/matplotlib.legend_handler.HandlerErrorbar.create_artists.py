    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):

        plotlines, caplines, barlinecols = orig_handle

        xdata, xdata_marker = self.get_xdata(legend, xdescent, ydescent,
                                             width, height, fontsize)

        ydata = ((height - ydescent) / 2.) * np.ones(xdata.shape, float)
        legline = Line2D(xdata, ydata)


        xdata_marker = np.asarray(xdata_marker)
        ydata_marker = np.asarray(ydata[:len(xdata_marker)])

        xerr_size, yerr_size = self.get_err_size(legend, xdescent, ydescent,
                                                 width, height, fontsize)

        legline_marker = Line2D(xdata_marker, ydata_marker)

        # when plotlines are None (only errorbars are drawn), we just
        # make legline invisible.
        if plotlines is None:
            legline.set_visible(False)
            legline_marker.set_visible(False)
        else:
            self.update_prop(legline, plotlines, legend)

            legline.set_drawstyle('default')
            legline.set_marker('None')

            self.update_prop(legline_marker, plotlines, legend)
            legline_marker.set_linestyle('None')

            if legend.markerscale != 1:
                newsz = legline_marker.get_markersize() * legend.markerscale
                legline_marker.set_markersize(newsz)

        handle_barlinecols = []
        handle_caplines = []

        if orig_handle.has_xerr:
            verts = [ ((x - xerr_size, y), (x + xerr_size, y))
                      for x, y in zip(xdata_marker, ydata_marker)]
            coll = mcoll.LineCollection(verts)
            self.update_prop(coll, barlinecols[0], legend)
            handle_barlinecols.append(coll)

            if caplines:
                capline_left = Line2D(xdata_marker - xerr_size, ydata_marker)
                capline_right = Line2D(xdata_marker + xerr_size, ydata_marker)
                self.update_prop(capline_left, caplines[0], legend)
                self.update_prop(capline_right, caplines[0], legend)
                capline_left.set_marker("|")
                capline_right.set_marker("|")

                handle_caplines.append(capline_left)
                handle_caplines.append(capline_right)

        if orig_handle.has_yerr:
            verts = [ ((x, y - yerr_size), (x, y + yerr_size))
                      for x, y in zip(xdata_marker, ydata_marker)]
            coll = mcoll.LineCollection(verts)
            self.update_prop(coll, barlinecols[0], legend)
            handle_barlinecols.append(coll)

            if caplines:
                capline_left = Line2D(xdata_marker, ydata_marker - yerr_size)
                capline_right = Line2D(xdata_marker, ydata_marker + yerr_size)
                self.update_prop(capline_left, caplines[0], legend)
                self.update_prop(capline_right, caplines[0], legend)
                capline_left.set_marker("_")
                capline_right.set_marker("_")

                handle_caplines.append(capline_left)
                handle_caplines.append(capline_right)

        artists = []
        artists.extend(handle_barlinecols)
        artists.extend(handle_caplines)
        artists.append(legline)
        artists.append(legline_marker)

        for artist in artists:
            artist.set_transform(trans)

        return artists

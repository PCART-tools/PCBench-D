    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):
        xdata, xdata_marker = self.get_xdata(legend, xdescent, ydescent,
                                             width, height, fontsize)

        ydata = self.get_ydata(legend, xdescent, ydescent,
                               width, height, fontsize)

        sizes = self.get_sizes(legend, orig_handle, xdescent, ydescent,
                               width, height, fontsize)

        p = self.create_collection(orig_handle, sizes,
                                   offsets=list(zip(xdata_marker, ydata)),
                                   transOffset=trans)

        self.update_prop(p, orig_handle, legend)
        p._transOffset = trans
        return [p]

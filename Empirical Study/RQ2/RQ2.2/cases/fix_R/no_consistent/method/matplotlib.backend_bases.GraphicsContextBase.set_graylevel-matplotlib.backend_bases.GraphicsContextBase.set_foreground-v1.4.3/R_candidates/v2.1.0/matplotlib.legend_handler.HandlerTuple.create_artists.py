    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize,
                       trans):

        handler_map = legend.get_legend_handler_map()

        if self._ndivide is None:
            ndivide = len(orig_handle)
        else:
            ndivide = self._ndivide

        if self._pad is None:
            pad = legend.borderpad * fontsize
        else:
            pad = self._pad * fontsize

        if ndivide > 1:
            width = (width - pad*(ndivide - 1)) / ndivide

        xds = [xdescent - (width + pad) * i for i in range(ndivide)]
        xds_cycle = cycle(xds)

        a_list = []
        for handle1 in orig_handle:
            handler = legend.get_legend_handler(handler_map, handle1)
            _a_list = handler.create_artists(legend, handle1,
                                             six.next(xds_cycle),
                                             ydescent,
                                             width, height,
                                             fontsize,
                                             trans)
            a_list.extend(_a_list)

        return a_list

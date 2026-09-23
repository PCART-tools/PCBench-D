    def _create_line(self, legend, orig_handle,
                     xdescent, ydescent, width, height, fontsize):

        # Overwrite manually because patch and line properties don't mix
        legline = Line2D([0, width], [height/2, height/2],
                         color=orig_handle.get_edgecolor(),
                         linestyle=orig_handle.get_linestyle(),
                         linewidth=orig_handle.get_linewidth(),
                         )

        legline.set_drawstyle('default')
        legline.set_marker("")
        return legline

class HandlerStepPatch(HandlerBase):
    """
    Handler for `~.matplotlib.patches.StepPatch` instances.
    """
    def __init__(self, **kw):
        """
        Any other keyword arguments are given to `HandlerBase`.
        """
        super().__init__(**kw)

    def _create_patch(self, legend, orig_handle,
                      xdescent, ydescent, width, height, fontsize):
        p = Rectangle(xy=(-xdescent, -ydescent),
                      color=orig_handle.get_facecolor(),
                      width=width, height=height)
        return p

    # Unfilled StepPatch should show as a line
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

    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        if orig_handle.get_fill() or (orig_handle.get_hatch() is not None):
            p = self._create_patch(legend, orig_handle,
                                   xdescent, ydescent, width, height, fontsize)
            self.update_prop(p, orig_handle, legend)
        else:
            p = self._create_line(legend, orig_handle,
                                  xdescent, ydescent, width, height, fontsize)
        p.set_transform(trans)
        return [p]

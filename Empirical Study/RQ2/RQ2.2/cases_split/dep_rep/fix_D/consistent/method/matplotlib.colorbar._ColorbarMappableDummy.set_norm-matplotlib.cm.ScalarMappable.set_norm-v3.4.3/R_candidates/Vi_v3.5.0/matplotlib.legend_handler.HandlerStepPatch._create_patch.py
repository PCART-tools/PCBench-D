    def _create_patch(self, legend, orig_handle,
                      xdescent, ydescent, width, height, fontsize):
        p = Rectangle(xy=(-xdescent, -ydescent),
                      color=orig_handle.get_facecolor(),
                      width=width, height=height)
        return p

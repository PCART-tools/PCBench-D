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

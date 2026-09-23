    def create_artists(self, legend, orig_handle,
                       xdescent, ydescent, width, height, fontsize, trans):
        # docstring inherited
        if orig_handle.get_fill() or (orig_handle.get_hatch() is not None):
            p = self._create_patch(orig_handle, xdescent, ydescent, width,
                                   height)
            self.update_prop(p, orig_handle, legend)
        else:
            p = self._create_line(orig_handle, width, height)
        p.set_transform(trans)
        return [p]

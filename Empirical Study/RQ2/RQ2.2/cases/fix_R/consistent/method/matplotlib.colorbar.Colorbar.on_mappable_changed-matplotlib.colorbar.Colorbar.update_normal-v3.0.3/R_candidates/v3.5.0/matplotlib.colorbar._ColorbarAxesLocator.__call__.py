    def __call__(self, ax, renderer):
        if self._orig_locator is not None:
            pos = self._orig_locator(ax, renderer)
        else:
            pos = ax.get_position(original=True)
        if self._cbar.extend == 'neither':
            return pos

        y, extendlen = self._cbar._proportional_y()
        if not self._cbar._extend_lower():
            extendlen[0] = 0
        if not self._cbar._extend_upper():
            extendlen[1] = 0
        len = sum(extendlen) + 1
        shrink = 1 / len
        offset = extendlen[0] / len
        # we need to reset the aspect ratio of the axes to account
        # of the extends...
        if hasattr(ax, '_colorbar_info'):
            aspect = ax._colorbar_info['aspect']
        else:
            aspect = False
        # now shrink and/or offset to take into account the
        # extend tri/rectangles.
        if self._cbar.orientation == 'vertical':
            if aspect:
                self._cbar.ax.set_box_aspect(aspect*shrink)
            pos = pos.shrunk(1, shrink).translated(0, offset * pos.height)
        else:
            if aspect:
                self._cbar.ax.set_box_aspect(1/(aspect * shrink))
            pos = pos.shrunk(shrink, 1).translated(offset * pos.width, 0)
        return pos

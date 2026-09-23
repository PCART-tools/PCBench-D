    def rgb_to_gdk_color(self, rgb):
        """
        rgb - an RGB tuple (three 0.0-1.0 values)
        return an allocated gtk.gdk.Color
        """
        try:
            return self._cached[tuple(rgb)]
        except KeyError:
            color = self._cached[tuple(rgb)] = \
                    self._cmap.alloc_color(
                        int(rgb[0]*65535),int(rgb[1]*65535),int(rgb[2]*65535))
            return color

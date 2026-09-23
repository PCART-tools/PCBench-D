    def reset_ticks(self):
        """
        Re-initialize the major and minor Tick lists.

        Each list starts with a single fresh Tick.
        """
        # Restore the lazy tick lists.
        try:
            del self.majorTicks
        except AttributeError:
            pass
        try:
            del self.minorTicks
        except AttributeError:
            pass
        try:
            self.set_clip_path(self.axes.patch)
        except AttributeError:
            pass

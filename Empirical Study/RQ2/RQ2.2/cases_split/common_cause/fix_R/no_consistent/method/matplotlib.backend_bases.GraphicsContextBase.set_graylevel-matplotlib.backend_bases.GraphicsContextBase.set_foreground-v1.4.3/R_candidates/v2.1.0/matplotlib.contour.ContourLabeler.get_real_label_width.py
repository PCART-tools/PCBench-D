    def get_real_label_width(self, lev, fmt, fsize):
        """
        This computes actual onscreen label width.
        This uses some black magic to determine onscreen extent of non-drawn
        label.  This magic may not be very robust.

        This method is not being used, and may be modified or removed.
        """
        # Find middle of axes
        xx = np.mean(np.asarray(self.ax.axis()).reshape(2, 2), axis=1)

        # Temporarily create text object
        t = text.Text(xx[0], xx[1])
        self.set_label_props(t, self.get_text(lev, fmt), 'k')

        # Some black magic to get onscreen extent
        # NOTE: This will only work for already drawn figures, as the canvas
        # does not have a renderer otherwise.  This is the reason this function
        # can't be integrated into the rest of the code.
        bbox = t.get_window_extent(renderer=self.ax.figure.canvas.renderer)

        # difference in pixel extent of image
        lw = np.diff(bbox.corners()[0::2, 0])[0]

        return lw

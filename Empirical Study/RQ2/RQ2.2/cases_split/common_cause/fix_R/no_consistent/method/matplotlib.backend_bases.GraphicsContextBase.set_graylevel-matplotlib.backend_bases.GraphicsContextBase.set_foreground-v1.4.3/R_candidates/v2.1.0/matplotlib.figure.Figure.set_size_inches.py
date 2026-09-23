    def set_size_inches(self, w, h=None, forward=True):
        """Set the figure size in inches (1in == 2.54cm)

        Usage ::

             fig.set_size_inches(w, h)  # OR
             fig.set_size_inches((w, h))

        optional kwarg *forward=True* will cause the canvas size to be
        automatically updated; e.g., you can resize the figure window
        from the shell

        ACCEPTS: a w, h tuple with w, h in inches

        See Also
        --------

        matplotlib.Figure.get_size_inches
        """

        # the width and height have been passed in as a tuple to the first
        # argument, so unpack them
        if h is None:
            w, h = w
        if not all(np.isfinite(_) for _ in (w, h)):
            raise ValueError('figure size must be finite not '
                             '({}, {})'.format(w, h))
        self.bbox_inches.p1 = w, h

        if forward:
            canvas = getattr(self, 'canvas')
            if canvas is not None:
                ratio = getattr(self.canvas, '_dpi_ratio', 1)
                dpival = self.dpi / ratio
                canvasw = w * dpival
                canvash = h * dpival
                manager = getattr(self.canvas, 'manager', None)
                if manager is not None:
                    manager.resize(int(canvasw), int(canvash))
        self.stale = True

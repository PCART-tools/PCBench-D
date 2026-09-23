    def set_markevery(self, every):
        """
        Set the markevery property to subsample the plot when using markers.

        e.g., if ``every=5``, every 5-th marker will be plotted.

        Parameters
        ----------
        every : None or int or (int, int) or slice or List[int] or float or \
(float, float) or List[bool]
            Which markers to plot.

            - every=None, every point will be plotted.
            - every=N, every N-th marker will be plotted starting with
              marker 0.
            - every=(start, N), every N-th marker, starting at point
              start, will be plotted.
            - every=slice(start, end, N), every N-th marker, starting at
              point start, up to but not including point end, will be plotted.
            - every=[i, j, m, n], only markers at points i, j, m, and n
              will be plotted.
            - every=[True, False, True], positions that are True will be
              plotted.
            - every=0.1, (i.e. a float) then markers will be spaced at
              approximately equal distances along the line; the distance
              along the line between markers is determined by multiplying the
              display-coordinate distance of the axes bounding-box diagonal
              by the value of every.
            - every=(0.5, 0.1) (i.e. a length-2 tuple of float), the same
              functionality as every=0.1 is exhibited but the first marker will
              be 0.5 multiplied by the display-coordinate-diagonal-distance
              along the line.

            For examples see
            :doc:`/gallery/lines_bars_and_markers/markevery_demo`.

        Notes
        -----
        Setting the markevery property will only show markers at actual data
        points.  When using float arguments to set the markevery property
        on irregularly spaced data, the markers will likely not appear evenly
        spaced because the actual data points do not coincide with the
        theoretical spacing between markers.

        When using a start offset to specify the first marker, the offset will
        be from the first data point which may be different from the first
        the visible data point if the plot is zoomed in.

        If zooming in on a plot when using float arguments then the actual
        data points that have markers will change because the distance between
        markers is always determined from the display-coordinates
        axes-bounding-box-diagonal regardless of the actual axes data limits.

        """
        self._markevery = every
        self.stale = True

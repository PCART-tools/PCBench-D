    def get_window_extent(self, renderer=None):
        '''
        Return a :class:`~matplotlib.transforms.Bbox` object bounding
        the text, in display units.

        In addition to being used internally, this is useful for
        specifying clickable regions in a png file on a web page.

        *renderer* defaults to the _renderer attribute of the text
        object.  This is not assigned until the first execution of
        :meth:`draw`, so you must use this kwarg if you want
        to call :meth:`get_window_extent` prior to the first
        :meth:`draw`.  For getting web page regions, it is
        simpler to call the method after saving the figure.
        '''
        self.update_coords(renderer)
        if self.get_dashlength() == 0.0:
            return Text.get_window_extent(self, renderer=renderer)
        else:
            return self._twd_window_extent

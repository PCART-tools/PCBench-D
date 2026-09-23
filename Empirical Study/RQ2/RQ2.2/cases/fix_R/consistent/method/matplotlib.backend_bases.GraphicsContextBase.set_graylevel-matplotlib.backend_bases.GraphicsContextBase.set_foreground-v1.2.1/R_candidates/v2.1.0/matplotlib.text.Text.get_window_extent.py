    def get_window_extent(self, renderer=None, dpi=None):
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

        *dpi* defaults to self.figure.dpi; the renderer dpi is
        irrelevant.  For the web application, if figure.dpi is not
        the value used when saving the figure, then the value that
        was used must be specified as the *dpi* argument.
        '''
        #return _unit_box
        if not self.get_visible():
            return Bbox.unit()
        if dpi is not None:
            dpi_orig = self.figure.dpi
            self.figure.dpi = dpi
        if self.get_text() == '':
            tx, ty = self._get_xy_display()
            return Bbox.from_bounds(tx, ty, 0, 0)

        if renderer is not None:
            self._renderer = renderer
        if self._renderer is None:
            raise RuntimeError('Cannot get window extent w/o renderer')

        bbox, info, descent = self._get_layout(self._renderer)
        x, y = self.get_unitless_position()
        x, y = self.get_transform().transform_point((x, y))
        bbox = bbox.translated(x, y)
        if dpi is not None:
            self.figure.dpi = dpi_orig
        return bbox

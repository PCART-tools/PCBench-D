    def __call__(self, axes, renderer):

        _xrefindex = self._axes_divider._xrefindex
        _yrefindex = self._axes_divider._yrefindex

        return self._axes_divider.locate(self._nx + _xrefindex,
                                         self._ny + _yrefindex,
                                         self._nx1 + _xrefindex,
                                         self._ny1 + _yrefindex,
                                         axes,
                                         renderer)

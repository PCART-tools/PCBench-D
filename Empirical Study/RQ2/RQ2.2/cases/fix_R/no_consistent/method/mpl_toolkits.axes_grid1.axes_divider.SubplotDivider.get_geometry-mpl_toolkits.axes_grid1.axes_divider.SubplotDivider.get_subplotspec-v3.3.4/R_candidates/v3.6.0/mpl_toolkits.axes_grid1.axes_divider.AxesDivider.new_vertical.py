    def new_vertical(self, size, pad=None, pack_start=False, **kwargs):
        """
        Helper method for ``append_axes("top")`` and ``append_axes("bottom")``.

        See the documentation of `append_axes` for more details.

        :meta private:
        """
        if pad is None:
            pad = mpl.rcParams["figure.subplot.hspace"] * self._yref
        if pad:
            if not isinstance(pad, Size._Base):
                pad = Size.from_any(pad, fraction_ref=self._yref)
            if pack_start:
                self._vertical.insert(0, pad)
                self._yrefindex += 1
            else:
                self._vertical.append(pad)
        if not isinstance(size, Size._Base):
            size = Size.from_any(size, fraction_ref=self._yref)
        if pack_start:
            self._vertical.insert(0, size)
            self._yrefindex += 1
            locator = self.new_locator(nx=self._xrefindex, ny=0)
        else:
            self._vertical.append(size)
            locator = self.new_locator(
                nx=self._xrefindex, ny=len(self._vertical) - 1)
        ax = self._get_new_axes(**kwargs)
        ax.set_axes_locator(locator)
        return ax

    def new_horizontal(self, size, pad=None, pack_start=False, **kwargs):
        """
        Helper method for ``append_axes("left")`` and ``append_axes("right")``.

        See the documentation of `append_axes` for more details.

        :meta private:
        """
        if pad is None:
            pad = mpl.rcParams["figure.subplot.wspace"] * self._xref
        if pad:
            if not isinstance(pad, Size._Base):
                pad = Size.from_any(pad, fraction_ref=self._xref)
            if pack_start:
                self._horizontal.insert(0, pad)
                self._xrefindex += 1
            else:
                self._horizontal.append(pad)
        if not isinstance(size, Size._Base):
            size = Size.from_any(size, fraction_ref=self._xref)
        if pack_start:
            self._horizontal.insert(0, size)
            self._xrefindex += 1
            locator = self.new_locator(nx=0, ny=self._yrefindex)
        else:
            self._horizontal.append(size)
            locator = self.new_locator(
                nx=len(self._horizontal) - 1, ny=self._yrefindex)
        ax = self._get_new_axes(**kwargs)
        ax.set_axes_locator(locator)
        return ax

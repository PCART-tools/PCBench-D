    def __getstate__(self):
        state = super().__getstate__()

        # The canvas cannot currently be pickled, but this has the benefit
        # of meaning that a figure can be detached from one canvas, and
        # re-attached to another.
        state.pop("canvas")

        # Set cached renderer to None -- it can't be pickled.
        state["_cachedRenderer"] = None

        # add version information to the state
        state['__mpl_version__'] = _mpl_version

        # check whether the figure manager (if any) is registered with pyplot
        from matplotlib import _pylab_helpers
        if getattr(self.canvas, 'manager', None) \
                in _pylab_helpers.Gcf.figs.values():
            state['_restore_to_pylab'] = True

        # set all the layoutbox information to None.  kiwisolver objects can't
        # be pickled, so we lose the layout options at this point.
        state.pop('_layoutbox', None)
        # suptitle:
        if self._suptitle is not None:
            self._suptitle._layoutbox = None

        return state

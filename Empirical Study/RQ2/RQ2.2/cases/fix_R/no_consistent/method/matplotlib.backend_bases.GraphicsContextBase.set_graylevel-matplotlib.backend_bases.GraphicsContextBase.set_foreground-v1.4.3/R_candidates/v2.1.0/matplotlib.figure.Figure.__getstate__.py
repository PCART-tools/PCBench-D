    def __getstate__(self):
        state = super(Figure, self).__getstate__()
        # the axobservers cannot currently be pickled.
        # Additionally, the canvas cannot currently be pickled, but this has
        # the benefit of meaning that a figure can be detached from one canvas,
        # and re-attached to another.
        for attr_to_pop in ('_axobservers', 'show',
                            'canvas', '_cachedRenderer'):
            state.pop(attr_to_pop, None)

        # add version information to the state
        state['__mpl_version__'] = _mpl_version

        # check to see if the figure has a manager and whether it is registered
        # with pyplot
        if getattr(self.canvas, 'manager', None) is not None:
            manager = self.canvas.manager
            import matplotlib._pylab_helpers
            if manager in list(six.itervalues(
                    matplotlib._pylab_helpers.Gcf.figs)):
                state['_restore_to_pylab'] = True

        return state

    @docstring.Substitution(x0=0.5, y0=0.98, name='suptitle', ha='center',
                            va='top')
    @docstring.copy(_suplabels)
    def suptitle(self, t, **kwargs):
        # docstring from _suplabels...
        info = {'name': '_suptitle', 'x0': 0.5, 'y0': 0.98,
                'ha': 'center', 'va': 'top', 'rotation': 0}
        return self._suplabels(t, info, **kwargs)

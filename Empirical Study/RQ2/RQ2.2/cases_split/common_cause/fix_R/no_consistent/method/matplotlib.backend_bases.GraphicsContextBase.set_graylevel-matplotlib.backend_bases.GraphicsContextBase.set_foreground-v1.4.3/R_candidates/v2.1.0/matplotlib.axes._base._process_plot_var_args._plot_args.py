    def _plot_args(self, tup, kwargs):
        ret = []
        if len(tup) > 1 and isinstance(tup[-1], six.string_types):
            linestyle, marker, color = _process_plot_format(tup[-1])
            tup = tup[:-1]
        elif len(tup) == 3:
            raise ValueError('third arg must be a format string')
        else:
            linestyle, marker, color = None, None, None

        # Don't allow any None value; These will be up-converted
        # to one element array of None which causes problems
        # downstream.
        if any(v is None for v in tup):
            raise ValueError("x and y must not be None")

        kw = {}
        for k, v in zip(('linestyle', 'marker', 'color'),
                        (linestyle, marker, color)):
            if v is not None:
                kw[k] = v

        if 'label' not in kwargs or kwargs['label'] is None:
            kwargs['label'] = get_label(tup[-1], None)

        if len(tup) == 2:
            x = _check_1d(tup[0])
            y = _check_1d(tup[-1])
        else:
            x, y = index_of(tup[-1])

        x, y = self._xy_from_xy(x, y)

        if self.command == 'plot':
            func = self._makeline
        else:
            kw['closed'] = kwargs.get('closed', True)
            func = self._makefill

        ncx, ncy = x.shape[1], y.shape[1]
        for j in xrange(max(ncx, ncy)):
            seg = func(x[:, j % ncx], y[:, j % ncy], kw, kwargs)
            ret.append(seg)
        return ret

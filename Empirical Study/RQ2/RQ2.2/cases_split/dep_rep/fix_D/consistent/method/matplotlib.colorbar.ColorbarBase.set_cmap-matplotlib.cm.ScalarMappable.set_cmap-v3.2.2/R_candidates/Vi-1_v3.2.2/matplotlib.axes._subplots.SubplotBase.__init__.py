    def __init__(self, fig, *args, **kwargs):
        """
        Parameters
        ----------
        fig : `matplotlib.figure.Figure`

        *args : tuple (*nrows*, *ncols*, *index*) or int
            The array of subplots in the figure has dimensions ``(nrows,
            ncols)``, and *index* is the index of the subplot being created.
            *index* starts at 1 in the upper left corner and increases to the
            right.

            If *nrows*, *ncols*, and *index* are all single digit numbers, then
            *args* can be passed as a single 3-digit number (e.g. 234 for
            (2, 3, 4)).
        """

        self.figure = fig

        if len(args) == 1:
            if isinstance(args[0], SubplotSpec):
                self._subplotspec = args[0]
            else:
                try:
                    s = str(int(args[0]))
                    rows, cols, num = map(int, s)
                except ValueError:
                    raise ValueError('Single argument to subplot must be '
                        'a 3-digit integer')
                self._subplotspec = GridSpec(rows, cols,
                                             figure=self.figure)[num - 1]
                # num - 1 for converting from MATLAB to python indexing
        elif len(args) == 3:
            rows, cols, num = args
            rows = int(rows)
            cols = int(cols)
            if rows <= 0:
                raise ValueError(f'Number of rows must be > 0, not {rows}')
            if cols <= 0:
                raise ValueError(f'Number of columns must be > 0, not {cols}')
            if isinstance(num, tuple) and len(num) == 2:
                num = [int(n) for n in num]
                self._subplotspec = GridSpec(
                        rows, cols,
                        figure=self.figure)[(num[0] - 1):num[1]]
            else:
                if num < 1 or num > rows*cols:
                    raise ValueError(
                        f"num must be 1 <= num <= {rows*cols}, not {num}")
                self._subplotspec = GridSpec(
                        rows, cols, figure=self.figure)[int(num) - 1]
                # num - 1 for converting from MATLAB to python indexing
        else:
            raise ValueError(f'Illegal argument(s) to subplot: {args}')

        self.update_params()

        # _axes_class is set in the subplot_class_factory
        self._axes_class.__init__(self, fig, self.figbox, **kwargs)
        # add a layout box to this, for both the full axis, and the poss
        # of the axis.  We need both because the axes may become smaller
        # due to parasitic axes and hence no longer fill the subplotspec.
        if self._subplotspec._layoutbox is None:
            self._layoutbox = None
            self._poslayoutbox = None
        else:
            name = self._subplotspec._layoutbox.name + '.ax'
            name = name + layoutbox.seq_id()
            self._layoutbox = layoutbox.LayoutBox(
                    parent=self._subplotspec._layoutbox,
                    name=name,
                    artist=self)
            self._poslayoutbox = layoutbox.LayoutBox(
                    parent=self._layoutbox,
                    name=self._layoutbox.name+'.pos',
                    pos=True, subplot=True, artist=self)

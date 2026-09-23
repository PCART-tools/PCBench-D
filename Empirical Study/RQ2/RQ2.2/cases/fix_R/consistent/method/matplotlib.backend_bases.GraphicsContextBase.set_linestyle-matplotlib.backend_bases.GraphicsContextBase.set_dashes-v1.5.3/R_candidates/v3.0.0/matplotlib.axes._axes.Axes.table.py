    @docstring.dedent_interpd
    def table(self, **kwargs):
        """
        Add a table to the current axes.

        Call signature::

          table(cellText=None, cellColours=None,
                cellLoc='right', colWidths=None,
                rowLabels=None, rowColours=None, rowLoc='left',
                colLabels=None, colColours=None, colLoc='center',
                loc='bottom', bbox=None)

        Returns a :class:`matplotlib.table.Table` instance. Either `cellText`
        or `cellColours` must be provided. For finer grained control over
        tables, use the :class:`~matplotlib.table.Table` class and add it to
        the axes with :meth:`~matplotlib.axes.Axes.add_table`.

        Thanks to John Gill for providing the class and table.

        kwargs control the :class:`~matplotlib.table.Table`
        properties:

        %(Table)s
        """
        return mtable.table(self, **kwargs)

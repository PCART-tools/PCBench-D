    def suptitle(self, t, **kwargs):
        """
        Add a centered title to the figure.

        kwargs are :class:`matplotlib.text.Text` properties.  Using figure
        coordinates, the defaults are:

          x : 0.5
            The x location of the text in figure coords

          y : 0.98
            The y location of the text in figure coords

          horizontalalignment : 'center'
            The horizontal alignment of the text

          verticalalignment : 'top'
            The vertical alignment of the text

        If the `fontproperties` keyword argument is given then the
        rcParams defaults for `fontsize` (`figure.titlesize`) and
        `fontweight` (`figure.titleweight`) will be ignored in favour
        of the `FontProperties` defaults.

        A :class:`matplotlib.text.Text` instance is returned.

        Example::

          fig.suptitle('this is the figure title', fontsize=12)
        """
        x = kwargs.pop('x', 0.5)
        y = kwargs.pop('y', 0.98)

        if ('horizontalalignment' not in kwargs) and ('ha' not in kwargs):
            kwargs['horizontalalignment'] = 'center'
        if ('verticalalignment' not in kwargs) and ('va' not in kwargs):
            kwargs['verticalalignment'] = 'top'

        if 'fontproperties' not in kwargs:
            if 'fontsize' not in kwargs and 'size' not in kwargs:
                kwargs['size'] = rcParams['figure.titlesize']
            if 'fontweight' not in kwargs and 'weight' not in kwargs:
                kwargs['weight'] = rcParams['figure.titleweight']

        sup = self.text(x, y, t, **kwargs)
        if self._suptitle is not None:
            self._suptitle.set_text(t)
            self._suptitle.set_position((x, y))
            self._suptitle.update_from(sup)
            sup.remove()
        else:
            self._suptitle = sup

        self.stale = True
        return self._suptitle

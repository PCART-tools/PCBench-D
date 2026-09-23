    def text(self, x, y, s, fontdict=None, withdash=False, **kwargs):
        """
        Add text to the axes.

        Add text in string `s` to axis at location `x`, `y`, data
        coordinates.

        Parameters
        ----------
        x, y : scalars
            data coordinates

        s : string
            text

        fontdict : dictionary, optional, default: None
            A dictionary to override the default text properties. If fontdict
            is None, the defaults are determined by your rc parameters.

        withdash : boolean, optional, default: False
            Creates a `~matplotlib.text.TextWithDash` instance instead of a
            `~matplotlib.text.Text` instance.

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.text.Text` properties.
            Other miscellaneous text parameters.

        Examples
        --------
        Individual keyword arguments can be used to override any given
        parameter::

            >>> text(x, y, s, fontsize=12)

        The default transform specifies that text is in data coords,
        alternatively, you can specify text in axis coords (0,0 is
        lower-left and 1,1 is upper-right).  The example below places
        text in the center of the axes::

            >>> text(0.5, 0.5,'matplotlib', horizontalalignment='center',
            ...      verticalalignment='center',
            ...      transform=ax.transAxes)

        You can put a rectangular box around the text instance (e.g., to
        set a background color) by using the keyword `bbox`.  `bbox` is
        a dictionary of `~matplotlib.patches.Rectangle`
        properties.  For example::

            >>> text(x, y, s, bbox=dict(facecolor='red', alpha=0.5))
        """
        default = {
            'verticalalignment': 'baseline',
            'horizontalalignment': 'left',
            'transform': self.transData,
            'clip_on': False}

        # At some point if we feel confident that TextWithDash
        # is robust as a drop-in replacement for Text and that
        # the performance impact of the heavier-weight class
        # isn't too significant, it may make sense to eliminate
        # the withdash kwarg and simply delegate whether there's
        # a dash to TextWithDash and dashlength.
        if withdash:
            t = mtext.TextWithDash(
                x=x, y=y, text=s)
        else:
            t = mtext.Text(
                x=x, y=y, text=s)

        t.update(default)
        if fontdict is not None:
            t.update(fontdict)
        t.update(kwargs)

        t.set_clip_path(self.patch)
        self._add_text(t)
        return t

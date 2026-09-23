    @docstring.dedent_interpd
    def text(self, x, y, s, fontdict=None, withdash=False, **kwargs):
        """
        Add text to figure.

        Parameters
        ----------
        x, y : float
            The position to place the text. By default, this is in figure
            coordinates, floats in [0, 1]. The coordinate system can be changed
            using the *transform* keyword.

        s : str
            The text string.

        fontdict : dictionary, optional, default: None
            A dictionary to override the default text properties. If fontdict
            is None, the defaults are determined by your rc parameters. A
            property in *kwargs* override the same property in fontdict.

        withdash : boolean, optional, default: False
            Creates a `~matplotlib.text.TextWithDash` instance instead of a
            `~matplotlib.text.Text` instance.

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.text.Text` properties
            Other miscellaneous text parameters.
            %(Text)s

        Returns
        -------
        text : `~.text.Text`

        See Also
        --------
        .Axes.text
        .pyplot.text
        """
        default = dict(transform=self.transFigure)

        if withdash:
            text = TextWithDash(x=x, y=y, text=s)
        else:
            text = Text(x=x, y=y, text=s)

        text.update(default)
        if fontdict is not None:
            text.update(fontdict)
        text.update(kwargs)

        text.set_figure(self)
        text.stale_callback = _stale_figure_callback

        self.texts.append(text)
        text._remove_method = self.texts.remove
        self.stale = True
        return text

    def set_title(self, label, fontdict=None, loc="center", **kwargs):
        """
        Set a title for the axes.

        Set one of the three available axes titles. The available titles
        are positioned above the axes in the center, flush with the left
        edge, and flush with the right edge.

        Parameters
        ----------
        label : str
            Text to use for the title

        fontdict : dict
            A dictionary controlling the appearance of the title text,
            the default `fontdict` is::

               {'fontsize': rcParams['axes.titlesize'],
                'fontweight' : rcParams['axes.titleweight'],
                'verticalalignment': 'baseline',
                'horizontalalignment': loc}

        loc : {'center', 'left', 'right'}, str, optional
            Which title to set, defaults to 'center'

        Returns
        -------
        text : :class:`~matplotlib.text.Text`
            The matplotlib text instance representing the title

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.text.Text` properties
            Other keyword arguments are text properties, see
            :class:`~matplotlib.text.Text` for a list of valid text
            properties.
        """
        try:
            title = {'left': self._left_title,
                     'center': self.title,
                     'right': self._right_title}[loc.lower()]
        except KeyError:
            raise ValueError("'%s' is not a valid location" % loc)
        default = {
            'fontsize': rcParams['axes.titlesize'],
            'fontweight': rcParams['axes.titleweight'],
            'verticalalignment': 'baseline',
            'horizontalalignment': loc.lower()}
        title.set_text(label)
        title.update(default)
        if fontdict is not None:
            title.update(fontdict)
        title.update(kwargs)
        return title

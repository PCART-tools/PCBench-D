    def set_title(self, label, fontdict=None, loc=None, pad=None,
                    **kwargs):
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
            the default *fontdict* is::

               {'fontsize': rcParams['axes.titlesize'],
                'fontweight' : rcParams['axes.titleweight'],
                'color' : rcParams['axes.titlecolor'],
                'verticalalignment': 'baseline',
                'horizontalalignment': loc}

        loc : {'center', 'left', 'right'}, str, optional
            Which title to set.
            If *None*, defaults to :rc:`axes.titlelocation`.

        pad : float
            The offset of the title from the top of the axes, in points.
            If *None*, defaults to :rc:`axes.titlepad`.

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
        if loc is None:
            loc = rcParams['axes.titlelocation']

        titles = {'left': self._left_title,
                  'center': self.title,
                  'right': self._right_title}
        title = cbook._check_getitem(titles, loc=loc.lower())
        default = {
            'fontsize': rcParams['axes.titlesize'],
            'fontweight': rcParams['axes.titleweight'],
            'verticalalignment': 'baseline',
            'horizontalalignment': loc.lower()}
        titlecolor = rcParams['axes.titlecolor']
        if not cbook._str_lower_equal(titlecolor, 'auto'):
            default["color"] = titlecolor
        if pad is None:
            pad = rcParams['axes.titlepad']
        self._set_title_offset_trans(float(pad))
        title.set_text(label)
        title.update(default)
        if fontdict is not None:
            title.update(fontdict)
        title.update(kwargs)
        return title

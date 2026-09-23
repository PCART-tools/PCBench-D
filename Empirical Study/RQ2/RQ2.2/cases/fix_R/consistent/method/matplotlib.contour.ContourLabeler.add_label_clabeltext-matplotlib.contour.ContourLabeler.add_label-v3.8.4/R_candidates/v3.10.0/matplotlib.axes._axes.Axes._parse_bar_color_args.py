    def _parse_bar_color_args(self, kwargs):
        """
        Helper function to process color-related arguments of `.Axes.bar`.

        Argument precedence for facecolors:

        - kwargs['facecolor']
        - kwargs['color']
        - 'Result of ``self._get_patches_for_fill.get_next_color``

        Argument precedence for edgecolors:

        - kwargs['edgecolor']
        - None

        Parameters
        ----------
        self : Axes

        kwargs : dict
            Additional kwargs. If these keys exist, we pop and process them:
            'facecolor', 'edgecolor', 'color'
            Note: The dict is modified by this function.


        Returns
        -------
        facecolor
            The facecolor. One or more colors as (N, 4) rgba array.
        edgecolor
            The edgecolor. Not normalized; may be any valid color spec or None.
        """
        color = kwargs.pop('color', None)

        facecolor = kwargs.pop('facecolor', color)
        edgecolor = kwargs.pop('edgecolor', None)

        facecolor = (facecolor if facecolor is not None
                     else self._get_patches_for_fill.get_next_color())

        try:
            facecolor = mcolors.to_rgba_array(facecolor)
        except ValueError as err:
            raise ValueError(
                "'facecolor' or 'color' argument must be a valid color or"
                    "sequence of colors."
            ) from err

        return facecolor, edgecolor

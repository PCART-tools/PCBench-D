    def suptitle(self, t, **kwargs):
        """
        Add a centered title to the figure.

        Parameters
        ----------
        t : str
            The title text.

        x : float, default 0.5
            The x location of the text in figure coordinates.

        y : float, default 0.98
            The y location of the text in figure coordinates.

        horizontalalignment, ha : {'center', 'left', right'}, default: 'center'
            The horizontal alignment of the text relative to (*x*, *y*).

        verticalalignment, va : {'top', 'center', 'bottom', 'baseline'}, \
default: 'top'
            The vertical alignment of the text relative to (*x*, *y*).

        fontsize, size : default: :rc:`figure.titlesize`
            The font size of the text. See `.Text.set_size` for possible
            values.

        fontweight, weight : default: :rc:`figure.titleweight`
            The font weight of the text. See `.Text.set_weight` for possible
            values.


        Returns
        -------
            text
                The `.Text` instance of the title.


        Other Parameters
        ----------------
        fontproperties : None or dict, optional
            A dict of font properties. If *fontproperties* is given the
            default values for font size and weight are taken from the
            `FontProperties` defaults. :rc:`figure.titlesize` and
            :rc:`figure.titleweight` are ignored in this case.

        **kwargs
            Additional kwargs are :class:`matplotlib.text.Text` properties.


        Examples
        --------
        >>> fig.suptitle('This is the figure title', fontsize=12)
        """
        manual_position = ('x' in kwargs or 'y' in kwargs)

        x = kwargs.pop('x', 0.5)
        y = kwargs.pop('y', 0.98)

        if 'horizontalalignment' not in kwargs and 'ha' not in kwargs:
            kwargs['horizontalalignment'] = 'center'
        if 'verticalalignment' not in kwargs and 'va' not in kwargs:
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
            self._suptitle._layoutbox = None
            if self._layoutbox is not None and not manual_position:
                w_pad, h_pad, wspace, hspace =  \
                        self.get_constrained_layout_pads(relative=True)
                figlb = self._layoutbox
                self._suptitle._layoutbox = layoutbox.LayoutBox(
                        parent=figlb, artist=self._suptitle,
                        name=figlb.name+'.suptitle')
                # stack the suptitle on top of all the children.
                # Some day this should be on top of all the children in the
                # gridspec only.
                for child in figlb.children:
                    if child is not self._suptitle._layoutbox:
                        layoutbox.vstack([self._suptitle._layoutbox,
                                          child],
                                         padding=h_pad*2., strength='required')
        self.stale = True
        return self._suptitle

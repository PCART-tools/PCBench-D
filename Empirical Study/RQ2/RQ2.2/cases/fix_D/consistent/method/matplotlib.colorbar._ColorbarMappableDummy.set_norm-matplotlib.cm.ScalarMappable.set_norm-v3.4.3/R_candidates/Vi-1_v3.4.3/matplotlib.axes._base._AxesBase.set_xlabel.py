    def set_xlabel(self, xlabel, fontdict=None, labelpad=None, *,
                   loc=None, **kwargs):
        """
        Set the label for the x-axis.

        Parameters
        ----------
        xlabel : str
            The label text.

        labelpad : float, default: :rc:`axes.labelpad`
            Spacing in points from the axes bounding box including ticks
            and tick labels.  If None, the previous value is left as is.

        loc : {'left', 'center', 'right'}, default: :rc:`xaxis.labellocation`
            The label position. This is a high-level alternative for passing
            parameters *x* and *horizontalalignment*.

        Other Parameters
        ----------------
        **kwargs : `.Text` properties
            `.Text` properties control the appearance of the label.

        See Also
        --------
        text : Documents the properties supported by `.Text`.
        """
        if labelpad is not None:
            self.xaxis.labelpad = labelpad
        protected_kw = ['x', 'horizontalalignment', 'ha']
        if {*kwargs} & {*protected_kw}:
            if loc is not None:
                raise TypeError(f"Specifying 'loc' is disallowed when any of "
                                f"its corresponding low level keyword "
                                f"arguments ({protected_kw}) are also "
                                f"supplied")
            loc = 'center'
        else:
            loc = (loc if loc is not None
                   else mpl.rcParams['xaxis.labellocation'])
        _api.check_in_list(('left', 'center', 'right'), loc=loc)
        if loc == 'left':
            kwargs.update(x=0, horizontalalignment='left')
        elif loc == 'right':
            kwargs.update(x=1, horizontalalignment='right')
        return self.xaxis.set_label_text(xlabel, fontdict, **kwargs)

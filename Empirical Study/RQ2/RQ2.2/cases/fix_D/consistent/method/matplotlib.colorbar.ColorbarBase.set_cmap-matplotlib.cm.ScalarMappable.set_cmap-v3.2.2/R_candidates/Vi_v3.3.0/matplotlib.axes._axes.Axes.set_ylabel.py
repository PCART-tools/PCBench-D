    def set_ylabel(self, ylabel, fontdict=None, labelpad=None, *,
                   loc=None, **kwargs):
        """
        Set the label for the y-axis.

        Parameters
        ----------
        ylabel : str
            The label text.

        labelpad : float, default: None
            Spacing in points from the axes bounding box including ticks
            and tick labels.

        loc : {'bottom', 'center', 'top'}, default: :rc:`yaxis.labellocation`
            The label position. This is a high-level alternative for passing
            parameters *y* and *horizontalalignment*.

        Other Parameters
        ----------------
        **kwargs : `.Text` properties
            `.Text` properties control the appearance of the label.

        See Also
        --------
        text : Documents the properties supported by `.Text`.
        """
        if labelpad is not None:
            self.yaxis.labelpad = labelpad
        protected_kw = ['y', 'horizontalalignment', 'ha']
        if {*kwargs} & {*protected_kw}:
            if loc is not None:
                raise TypeError(f"Specifying 'loc' is disallowed when any of "
                                f"its corresponding low level keyword "
                                f"arguments ({protected_kw}) are also "
                                f"supplied")
            loc = 'center'
        else:
            loc = loc if loc is not None else rcParams['yaxis.labellocation']
        cbook._check_in_list(('bottom', 'center', 'top'), loc=loc)
        if loc == 'bottom':
            kwargs.update(y=0, horizontalalignment='left')
        elif loc == 'top':
            kwargs.update(y=1, horizontalalignment='right')
        return self.yaxis.set_label_text(ylabel, fontdict, **kwargs)

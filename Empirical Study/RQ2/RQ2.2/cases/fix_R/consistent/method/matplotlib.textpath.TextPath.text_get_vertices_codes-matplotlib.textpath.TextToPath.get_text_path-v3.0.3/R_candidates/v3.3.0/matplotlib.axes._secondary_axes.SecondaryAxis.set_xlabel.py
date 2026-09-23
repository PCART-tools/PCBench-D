    def set_xlabel(self, xlabel, fontdict=None, labelpad=None, **kwargs):
        """
        Set the label for the x-axis.

        Parameters
        ----------
        xlabel : str
            The label text.

        labelpad : float, default: ``self.xaxis.labelpad``
            Spacing in points between the label and the x-axis.

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
        return self.xaxis.set_label_text(xlabel, fontdict, **kwargs)

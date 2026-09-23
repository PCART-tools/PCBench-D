    def set_xlabel(self, xlabel, fontdict=None, labelpad=None, **kwargs):
        """
        Set the label for the xaxis.

        Parameters
        ----------
        xlabel : string
            x label

        labelpad : scalar, optional, default: None
            spacing in points between the label and the x-axis

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.text.Text` properties

        See also
        --------
        text : for information on how override and the optional args work
        """
        if labelpad is not None:
            self.xaxis.labelpad = labelpad
        return self.xaxis.set_label_text(xlabel, fontdict, **kwargs)

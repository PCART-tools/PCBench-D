    def set_ylabel(self, ylabel, fontdict=None, labelpad=None, **kwargs):
        """
        Set the label for the yaxis

        Parameters
        ----------
        ylabel : string
            y label

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
            self.yaxis.labelpad = labelpad
        return self.yaxis.set_label_text(ylabel, fontdict, **kwargs)

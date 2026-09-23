    def set_label_text(self, label, fontdict=None, **kwargs):
        """
        Set the text value of the axis label.

        Parameters
        ----------
        label : str
            Text string.
        fontdict : dict
            Text properties.
        **kwargs
            Merged into fontdict.
        """
        self.isDefault_label = False
        self.label.set_text(label)
        if fontdict is not None:
            self.label.update(fontdict)
        self.label.update(kwargs)
        self.stale = True
        return self.label

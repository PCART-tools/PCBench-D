    @_api.deprecated("3.6", alternative='set_label_minor()')
    def label_minor(self, labelOnlyBase):
        """
        Switch minor tick labeling on or off.

        Parameters
        ----------
        labelOnlyBase : bool
            If True, label ticks only at integer powers of base.
        """
        self.set_label_minor(labelOnlyBase)

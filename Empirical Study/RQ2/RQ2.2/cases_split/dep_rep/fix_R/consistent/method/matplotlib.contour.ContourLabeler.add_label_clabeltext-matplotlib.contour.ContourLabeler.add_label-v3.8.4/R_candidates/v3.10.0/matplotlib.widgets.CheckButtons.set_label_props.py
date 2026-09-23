    def set_label_props(self, props):
        """
        Set properties of the `.Text` labels.

        .. versionadded:: 3.7

        Parameters
        ----------
        props : dict
            Dictionary of `.Text` properties to be used for the labels.
        """
        _api.check_isinstance(dict, props=props)
        props = _expand_text_props(props)
        for text, prop in zip(self.labels, props):
            text.update(prop)

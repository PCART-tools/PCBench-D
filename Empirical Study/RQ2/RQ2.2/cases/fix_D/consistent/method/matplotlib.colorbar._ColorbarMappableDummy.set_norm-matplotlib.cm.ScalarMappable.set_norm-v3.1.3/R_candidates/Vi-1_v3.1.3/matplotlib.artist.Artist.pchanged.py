    def pchanged(self):
        """
        Call all of the registered callbacks.

        This function is triggered internally when a property is changed.

        See Also
        --------
        add_callback
        remove_callback
        """
        for oid, func in self._propobservers.items():
            func(self)

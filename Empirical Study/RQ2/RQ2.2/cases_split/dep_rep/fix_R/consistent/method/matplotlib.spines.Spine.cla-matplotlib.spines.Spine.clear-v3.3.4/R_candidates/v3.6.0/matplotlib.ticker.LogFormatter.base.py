    @_api.deprecated("3.6", alternative='set_base()')
    def base(self, base):
        """
        Change the *base* for labeling.

        .. warning::
           Should always match the base used for :class:`LogLocator`
        """
        self.set_base(base)

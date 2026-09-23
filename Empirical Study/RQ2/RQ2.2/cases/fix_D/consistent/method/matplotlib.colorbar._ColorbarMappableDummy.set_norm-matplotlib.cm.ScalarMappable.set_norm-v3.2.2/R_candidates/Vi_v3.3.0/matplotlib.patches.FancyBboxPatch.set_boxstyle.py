    @docstring.dedent_interpd
    def set_boxstyle(self, boxstyle=None, **kwargs):
        """
        Set the box style.

        Most box styles can be further configured using attributes.
        Attributes from the previous box style are not reused.

        Without argument (or with ``boxstyle=None``), the available box styles
        are returned as a human-readable string.

        Parameters
        ----------
        boxstyle : str
            The name of the box style. Optionally, followed by a comma and a
            comma-separated list of attributes. The attributes may
            alternatively be passed separately as keyword arguments.

            The following box styles are available:

            %(AvailableBoxstyles)s

            .. ACCEPTS: %(ListBoxstyles)s

        **kwargs
            Additional attributes for the box style. See the table above for
            supported parameters.

        Examples
        --------
        ::

            set_boxstyle("round,pad=0.2")
            set_boxstyle("round", pad=0.2)

        """
        if boxstyle is None:
            return BoxStyle.pprint_styles()

        if isinstance(boxstyle, BoxStyle._Base) or callable(boxstyle):
            self._bbox_transmuter = boxstyle
        else:
            self._bbox_transmuter = BoxStyle(boxstyle, **kwargs)
        self.stale = True

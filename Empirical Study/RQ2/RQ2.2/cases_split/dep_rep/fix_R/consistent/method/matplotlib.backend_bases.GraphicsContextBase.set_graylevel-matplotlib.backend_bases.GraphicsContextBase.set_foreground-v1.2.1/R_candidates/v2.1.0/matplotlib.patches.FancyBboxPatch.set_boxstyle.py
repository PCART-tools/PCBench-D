    @docstring.dedent_interpd
    def set_boxstyle(self, boxstyle=None, **kw):
        """
        Set the box style.

        *boxstyle* can be a string with boxstyle name with optional
        comma-separated attributes. Alternatively, the attrs can
        be provided as keywords::

            set_boxstyle("round,pad=0.2")
            set_boxstyle("round", pad=0.2)

        Old attrs simply are forgotten.

        Without argument (or with *boxstyle* = None), it returns
        available box styles.

        The following boxstyles are available:
        %(AvailableBoxstyles)s

        ACCEPTS: %(ListBoxstyles)s

        """
        if boxstyle is None:
            return BoxStyle.pprint_styles()

        if isinstance(boxstyle, BoxStyle._Base) or callable(boxstyle):
            self._bbox_transmuter = boxstyle
        else:
            self._bbox_transmuter = BoxStyle(boxstyle, **kw)
        self.stale = True

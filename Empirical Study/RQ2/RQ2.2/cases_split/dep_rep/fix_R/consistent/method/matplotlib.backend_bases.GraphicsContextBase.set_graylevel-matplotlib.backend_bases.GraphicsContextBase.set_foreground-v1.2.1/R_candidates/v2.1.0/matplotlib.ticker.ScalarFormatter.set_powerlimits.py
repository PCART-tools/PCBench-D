    def set_powerlimits(self, lims):
        """
        Sets size thresholds for scientific notation.

        ``lims`` is a two-element sequence containing the powers of 10
        that determine the switchover threshold. Numbers below
        ``10**lims[0]`` and above ``10**lims[1]`` will be displayed in
        scientific notation.

        For example, ``formatter.set_powerlimits((-3, 4))`` sets the
        pre-2007 default in which scientific notation is used for
        numbers less than 1e-3 or greater than 1e4.

        .. seealso:: Method :meth:`set_scientific`
        """
        if len(lims) != 2:
            raise ValueError("'lims' must be a sequence of length 2")
        self._powerlimits = lims

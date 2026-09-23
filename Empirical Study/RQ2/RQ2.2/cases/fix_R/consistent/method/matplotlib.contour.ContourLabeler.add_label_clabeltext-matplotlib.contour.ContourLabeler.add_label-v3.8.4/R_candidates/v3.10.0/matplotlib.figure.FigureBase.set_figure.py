    def set_figure(self, fig):
        """
        .. deprecated:: 3.10
            Currently this method will raise an exception if *fig* is anything other
            than the root `.Figure` this (Sub)Figure is on.  In future it will always
            raise an exception.
        """
        no_switch = ("The parent and root figures of a (Sub)Figure are set at "
                     "instantiation and cannot be changed.")
        if fig is self._root_figure:
            _api.warn_deprecated(
                "3.10",
                message=(f"{no_switch} From Matplotlib 3.12 this operation will raise "
                         "an exception."))
            return

        raise ValueError(no_switch)

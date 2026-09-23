    def set_check_props(self, props):
        """
        Set properties of the check button checks.

        .. versionadded:: 3.7

        Parameters
        ----------
        props : dict
            Dictionary of `.Collection` properties to be used for the check
            button check.
        """
        _api.check_isinstance(dict, props=props)
        if 's' in props:  # Keep API consistent with constructor.
            props['sizes'] = np.broadcast_to(props.pop('s'), len(self.labels))
        actives = self.get_status()
        self._checks.update(props)
        # If new colours are supplied, then we must re-apply the status.
        self._init_status(actives)

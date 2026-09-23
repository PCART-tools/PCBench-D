    def set_picker(self, p):
        # docstring inherited
        if isinstance(p, Number) and not isinstance(p, bool):
            # After deprecation, the whole method can be deleted and inherited.
            cbook.warn_deprecated(
                "3.3", message="Setting the line's pick radius via set_picker "
                "is deprecated since %(since)s and will be removed "
                "%(removal)s; use set_pickradius instead.")
            self.pickradius = p
        self._picker = p

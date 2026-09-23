    def __setattr__(self, name, value):
        """After regular attribute access, try looking up the name of the info
        This allows simpler access to columns for interactive use."""
        if name in self._internal_names_set:
            object.__setattr__(self, name, value)
        else:
            try:
                existing = getattr(self, name)
                if isinstance(existing, Index):
                    object.__setattr__(self, name, value)
                elif name in self._info_axis:
                    self[name] = value
                else:
                    object.__setattr__(self, name, value)
            except (AttributeError, TypeError):
                object.__setattr__(self, name, value)

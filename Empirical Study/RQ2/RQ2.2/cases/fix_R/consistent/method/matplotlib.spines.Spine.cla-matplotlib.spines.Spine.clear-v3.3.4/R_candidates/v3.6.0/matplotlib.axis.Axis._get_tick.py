    def _get_tick(self, major):
        """Return the default tick instance."""
        if self._tick_class is None:
            raise NotImplementedError(
                f"The Axis subclass {self.__class__.__name__} must define "
                "_tick_class or reimplement _get_tick()")
        tick_kw = self._major_tick_kw if major else self._minor_tick_kw
        return self._tick_class(self.axes, 0, major=major, **tick_kw)

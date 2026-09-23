    @final
    def _construct_axes_dict(self, axes: Sequence[Axis] | None = None, **kwargs):
        """Return an axes dictionary for myself."""
        d = {a: self._get_axis(a) for a in (axes or self._AXIS_ORDERS)}
        # error: Argument 1 to "update" of "MutableMapping" has incompatible type
        # "Dict[str, Any]"; expected "SupportsKeysAndGetItem[Union[int, str], Any]"
        d.update(kwargs)  # type: ignore[arg-type]
        return d

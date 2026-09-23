    def _set_converter(self, converter):
        if self._converter is converter or self._converter == converter:
            return
        if self._converter_is_explicit:
            raise RuntimeError("Axis already has an explicit converter set")
        elif (
            self._converter is not None and
            not isinstance(converter, type(self._converter)) and
            not isinstance(self._converter, type(converter))
        ):
            _api.warn_external(
                "This axis already has a converter set and "
                "is updating to a potentially incompatible converter"
            )
        self._converter = converter

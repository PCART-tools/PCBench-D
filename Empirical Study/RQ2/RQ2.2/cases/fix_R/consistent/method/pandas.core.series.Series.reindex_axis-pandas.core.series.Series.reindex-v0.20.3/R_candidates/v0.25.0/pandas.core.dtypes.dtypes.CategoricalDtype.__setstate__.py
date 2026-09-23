    def __setstate__(self, state: Dict[str_type, Any]) -> None:
        # for pickle compat. __get_state__ is defined in the
        # PandasExtensionDtype superclass and uses the public properties to
        # pickle -> need to set the settable private ones here (see GH26067)
        self._categories = state.pop("categories", None)
        self._ordered = state.pop("ordered", False)
        self._ordered_from_sentinel = state.pop("_ordered_from_sentinel", False)

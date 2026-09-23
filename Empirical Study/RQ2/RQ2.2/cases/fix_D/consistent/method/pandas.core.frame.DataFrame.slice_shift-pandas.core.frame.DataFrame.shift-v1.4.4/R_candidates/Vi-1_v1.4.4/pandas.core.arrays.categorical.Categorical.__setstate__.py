    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        if not isinstance(state, dict):
            return super().__setstate__(state)

        if "_dtype" not in state:
            state["_dtype"] = CategoricalDtype(state["_categories"], state["_ordered"])

        if "_codes" in state and "_ndarray" not in state:
            # backward compat, changed what is property vs attribute
            state["_ndarray"] = state.pop("_codes")

        super().__setstate__(state)

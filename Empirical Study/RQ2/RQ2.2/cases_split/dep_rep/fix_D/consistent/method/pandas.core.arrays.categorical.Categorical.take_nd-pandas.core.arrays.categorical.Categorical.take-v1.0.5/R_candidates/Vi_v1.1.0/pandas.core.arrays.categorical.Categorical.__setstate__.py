    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        if not isinstance(state, dict):
            raise Exception("invalid pickle state")

        if "_dtype" not in state:
            state["_dtype"] = CategoricalDtype(state["_categories"], state["_ordered"])

        for k, v in state.items():
            setattr(self, k, v)

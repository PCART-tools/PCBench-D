    @final
    def __setstate__(self, state):
        if isinstance(state, BlockManager):
            self._mgr = state
        elif isinstance(state, dict):
            if "_data" in state and "_mgr" not in state:
                # compat for older pickles
                state["_mgr"] = state.pop("_data")
            typ = state.get("_typ")
            if typ is not None:
                attrs = state.get("_attrs", {})
                object.__setattr__(self, "_attrs", attrs)
                flags = state.get("_flags", {"allows_duplicate_labels": True})
                object.__setattr__(self, "_flags", Flags(self, **flags))

                # set in the order of internal names
                # to avoid definitional recursion
                # e.g. say fill_value needing _mgr to be
                # defined
                meta = set(self._internal_names + self._metadata)
                for k in list(meta):
                    if k in state and k != "_flags":
                        v = state[k]
                        object.__setattr__(self, k, v)

                for k, v in state.items():
                    if k not in meta:
                        object.__setattr__(self, k, v)

            else:
                raise NotImplementedError("Pre-0.12 pickles are no longer supported")
        elif len(state) == 2:
            raise NotImplementedError("Pre-0.12 pickles are no longer supported")

        self._item_cache = {}

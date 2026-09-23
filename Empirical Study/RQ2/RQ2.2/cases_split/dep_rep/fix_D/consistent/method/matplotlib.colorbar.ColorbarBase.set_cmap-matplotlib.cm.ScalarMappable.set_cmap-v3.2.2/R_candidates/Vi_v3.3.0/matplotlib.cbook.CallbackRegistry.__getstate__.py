    def __getstate__(self):
        # In general, callbacks may not be pickled, so we just drop them.
        return {**vars(self), "callbacks": {}, "_func_cid_map": {}}

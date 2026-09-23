    def __getstate__(self):
        state = self.__dict__.copy()
        state["_data"] = self._data.combine_chunks()
        return state

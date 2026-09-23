    def __getstate__(self):
        state = self.__dict__.copy()
        state["_pa_array"] = self._pa_array.combine_chunks()
        return state

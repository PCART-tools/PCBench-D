    def __setstate__(self, state) -> None:
        if "_data" in state:
            data = state.pop("_data")
        else:
            data = state["_pa_array"]
        state["_pa_array"] = pa.chunked_array(data)
        self.__dict__.update(state)

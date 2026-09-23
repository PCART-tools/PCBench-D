    def __setstate__(self, state) -> None:
        state["_data"] = pa.chunked_array(state["_data"])
        self.__dict__.update(state)

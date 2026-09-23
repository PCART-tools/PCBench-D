    def _unpickle_matrix_compat(self, state):  # pragma: no cover
        # old unpickling
        (vals, idx, cols), object_state = state

        index = com._unpickle_array(idx)
        dm = DataFrame(vals, index=index, columns=com._unpickle_array(cols),
                       copy=False)

        if object_state is not None:
            ovals, _, ocols = object_state
            objects = DataFrame(ovals, index=index,
                                columns=com._unpickle_array(ocols), copy=False)

            dm = dm.join(objects)

        self._data = dm._data

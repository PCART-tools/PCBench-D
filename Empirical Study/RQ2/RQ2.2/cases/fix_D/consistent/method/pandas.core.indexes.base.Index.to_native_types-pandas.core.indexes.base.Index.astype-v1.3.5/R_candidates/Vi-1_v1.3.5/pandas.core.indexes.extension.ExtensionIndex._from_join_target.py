    def _from_join_target(self, result: np.ndarray) -> ArrayLike:
        # ATM this is only for IntervalIndex, implicit assumption
        #  about _get_engine_target
        return type(self._data)._from_sequence(result, dtype=self.dtype)

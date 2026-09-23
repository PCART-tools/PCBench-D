    @property
    def codes(self) -> npt.NDArray[np.signedinteger]:
        if self._codes is not None:
            # _codes is set in __init__ for MultiIndex cases
            return self._codes

        return self._codes_and_uniques[0]

    @property
    def codes(self) -> npt.NDArray[np.signedinteger]:
        return self._codes_and_uniques[0]

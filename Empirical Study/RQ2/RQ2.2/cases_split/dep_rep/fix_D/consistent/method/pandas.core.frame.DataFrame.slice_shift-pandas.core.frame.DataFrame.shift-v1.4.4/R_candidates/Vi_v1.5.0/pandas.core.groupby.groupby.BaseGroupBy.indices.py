    @final
    @property
    def indices(self) -> dict[Hashable, npt.NDArray[np.intp]]:
        """
        Dict {group name -> group indices}.
        """
        return self.grouper.indices

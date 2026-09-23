    @final
    @property
    def groups(self) -> dict[Hashable, np.ndarray]:
        """
        Dict {group name -> group labels}.
        """
        return self.grouper.groups

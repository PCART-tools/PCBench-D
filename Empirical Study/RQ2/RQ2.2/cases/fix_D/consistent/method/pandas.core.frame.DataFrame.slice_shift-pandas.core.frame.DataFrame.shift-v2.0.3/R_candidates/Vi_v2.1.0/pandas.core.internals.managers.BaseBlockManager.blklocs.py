    @property
    def blklocs(self) -> npt.NDArray[np.intp]:
        """
        See blknos.__doc__
        """
        if self._blklocs is None:
            # Note: these can be altered by other BlockManager methods.
            self._rebuild_blknos_and_blklocs()

        return self._blklocs

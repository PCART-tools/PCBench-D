    def __dlpack__(self) -> Any:
        """
        Represent this structure as DLPack interface.
        """
        if _NUMPY_HAS_DLPACK:
            return self._x.__dlpack__()
        raise NotImplementedError("__dlpack__")

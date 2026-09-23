    @abstractmethod
    def __dlpack__(self):
        """
        Produce DLPack capsule (see array API standard).

        Raises:

            - TypeError : if the buffer contains unsupported dtypes.
            - NotImplementedError : if DLPack support is not implemented

        Useful to have to connect to array libraries. Support optional because
        it's not completely trivial to implement for a Python-only library.
        """
        raise NotImplementedError("__dlpack__")

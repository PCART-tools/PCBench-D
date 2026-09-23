    @staticmethod
    def new(ex: BaseException) -> Any:
        """
        Creates an object that raises the wrapped exception ``ex`` when used,
        and casts it to :py:obj:`~typing.Any` type.
        """
        return DeferredError(ex)

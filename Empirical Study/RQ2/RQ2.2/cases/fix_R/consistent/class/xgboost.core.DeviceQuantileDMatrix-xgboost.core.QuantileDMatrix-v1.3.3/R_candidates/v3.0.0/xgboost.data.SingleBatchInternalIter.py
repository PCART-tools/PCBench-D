class SingleBatchInternalIter(DataIter):  # pylint: disable=R0902
    """An iterator for single batch data to help creating device DMatrix.
    Transforming input directly to histogram with normal single batch data API
    can not access weight for sketching.  So this iterator acts as a staging
    area for meta info.

    """

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.it = 0  # pylint: disable=invalid-name

        # This does not necessarily increase memory usage as the data transformation
        # might use memory.
        super().__init__(release_data=False)

    def next(self, input_data: Callable) -> bool:
        if self.it == 1:
            return False
        self.it += 1
        input_data(**self.kwargs)
        return True

    def reset(self) -> None:
        self.it = 0

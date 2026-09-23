class _SklObjWProto(Protocol):
    def __call__(
        self,
        y_true: ArrayLike,
        y_pred: ArrayLike,
        sample_weight: Optional[ArrayLike],
    ) -> Tuple[ArrayLike, ArrayLike]: ...

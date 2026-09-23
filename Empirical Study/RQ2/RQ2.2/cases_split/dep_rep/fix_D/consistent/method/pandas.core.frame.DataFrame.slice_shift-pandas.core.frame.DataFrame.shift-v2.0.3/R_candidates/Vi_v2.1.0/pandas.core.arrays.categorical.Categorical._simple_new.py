    @classmethod
    # error: Argument 2 of "_simple_new" is incompatible with supertype
    # "NDArrayBacked"; supertype defines the argument type as
    # "Union[dtype[Any], ExtensionDtype]"
    def _simple_new(  # type: ignore[override]
        cls, codes: np.ndarray, dtype: CategoricalDtype
    ) -> Self:
        # NB: This is not _quite_ as simple as the "usual" _simple_new
        codes = coerce_indexer_dtype(codes, dtype.categories)
        dtype = CategoricalDtype(ordered=False).update_dtype(dtype)
        return super()._simple_new(codes, dtype)
